from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.bitcointrading.tools.technical_tools.indicators import CALCULATE_INDICATORS
from src.bitcointrading.tools.research_tools.scraping import GET_NEWS
import yaml

@CrewBase
class BitcoinTrading():
    """Bitcoin Trading Analysis Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
 
    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            verbose=True,
        )

    @agent
    def technical_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_analyst_agent"],
            verbose=True,
        )

    @agent
    def decider(self) -> Agent:
        return Agent(
            config=self.agents_config["decider_agent"],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["researcher_task"],
            agent=self.research_agent(),
            output_file='market_research.md',
        )

    @task
    def technical_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["technical_analysis_task"],
            agent=self.technical_analyst(),
            output_file='technical_analysis.md',
        )

    @task
    def decision_task(self) -> Task:
        return Task(
            config=self.tasks_config["decision_task"],
            agent=self.decider(),
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
