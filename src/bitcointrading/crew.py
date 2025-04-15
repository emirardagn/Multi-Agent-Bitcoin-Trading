from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.bitcointrading.tools.technical_tools.indicators import CALCULATE_INDICATORS
from src.bitcointrading.tools.research_tools.scraping import GET_NEWS
@CrewBase
class Bitcointrading():
    """Bitcoin Trading Analysis Crew"""

    agents_config = 'src/bitcointrading/config/agents.yaml'
    tasks_config = 'src/bitcointrading/config/tasks.yaml'

    get_news = GET_NEWS()
    calculate_indicators = CALCULATE_INDICATORS()
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[self.get_news]
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            tools=[self.calculate_indicators]
        )

    @agent
    def decider(self) -> Agent:
        return Agent(
            config=self.agents_config['decider'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            output_file='market_research.md',
        )

    @task
    def technical_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_analysis_task'],
            output_file='technical_analysis.md',
        )

    @task
    def decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['decision_task'],
            output_file='trading_decision.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Bitcoin Trading Analysis crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
