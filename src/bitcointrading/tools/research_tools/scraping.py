import requests
from bs4 import BeautifulSoup
import json
import yaml
import random
import os
from crewai.tools import tool

# Get the absolute path to the parameters file
parameters = yaml.safe_load(open('src/bitcointrading/config/parameters.yaml'))["research"]

MAX_ARTICLES_PER_SOURCE = parameters['MAX_ARTICLES_PER_SOURCE']
HEADERS = parameters['HEADERS']
DISCLAIMERS = parameters['DISCLAIMERS']



def get_cointelegraph_news():
    news = []
    url = "https://cointelegraph.com/tags/markets"
    response = requests.get(url, headers=random.choice(HEADERS))
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find('div', class_='tag-page__rows')
    articles = container.find_all('div', class_='post-card-inline__header')
    if len(articles) > MAX_ARTICLES_PER_SOURCE:
        articles = articles[0:MAX_ARTICLES_PER_SOURCE]
    
    for article in articles:
        title = article.find('span').text if article.find('span') else ''
        article_url = article.find('a')['href'] if article.find('a') else ''
        article_url = "https://cointelegraph.com" + article_url
        
        response = requests.get(article_url, headers=random.choice(HEADERS))
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('div', class_='post-content relative')
        text = content.find_all('p')
        text = [p.text for p in text]
        content = ' '.join(text)
      
        for disclaimer in DISCLAIMERS:
            if disclaimer in content:
                content = content[:content.find(disclaimer)]

        news.append({
            'title': title.replace('\n', ' ').replace('\r', ' ').strip(),
            'content': content.replace('\n', ' ').replace('\r', ' ').strip(),
            'source': 'cointelegraph'
        })
    return news

def get_cryptonews_news():
    url = "https://crypto.news/tag/bitcoin/"
    news = []
    response = requests.get(url, headers=random.choice(HEADERS))
    soup = BeautifulSoup(response.text, 'html.parser')
    container = soup.find('div', class_='tag-archive__content')
    articles = container.find_all('p', class_='post-loop__title')

    if len(articles) > MAX_ARTICLES_PER_SOURCE:
        articles = articles[0:MAX_ARTICLES_PER_SOURCE]

    for article in articles:
        title = article.find('a').text if article.find('a') else ''
        article_url = article.find('a')['href'] if article.find('a') else ''
        article_url = article_url
        response = requests.get(article_url, headers=random.choice(HEADERS))
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='post-detail__content blocks')
        text = content.find_all('p')
        text = [p.text for p in text]
        content = ' '.join(text)
        
        news.append({
            'title': title.replace('\n', ' ').replace('\r', ' ').strip(),
            'content': content.replace('\n', ' ').replace('\r', ' ').strip(),
            'source': 'cryptonews'
        })
    return news

#Main Function That Scrapes News From Major Sources -> tool for research
@tool("Scrape cryptocurrency news from major sources")
def GET_NEWS() -> list:
    """Useful for gathering the latest cryptocurrency news and market updates from major sources like Cointelegraph and Cryptonews.
    Returns a list of news articles with their titles, content, and sources."""
    cointelegraph_news = get_cointelegraph_news()
    cryptonews_news = get_cryptonews_news()
    all_news = cointelegraph_news + cryptonews_news
    
    with open('outputs/news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    return all_news
