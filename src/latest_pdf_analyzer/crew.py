import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew

load_dotenv()

# Create LLM using Groq model
llm = LLM(
    model=os.getenv("MODEL"),
    temperature=0.3
)


@CrewBase
class ResumeAnalyzerCrew:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_analyst"],
            llm=llm
        )

    @agent
    def hr_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_evaluator"],
            llm=llm
        )

    @task
    def analyze_resume(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_resume"],
            agent=self.resume_analyst()
        )

    @task
    def evaluate_resume(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_resume"],
            agent=self.hr_evaluator(),
            context=[self.analyze_resume()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            tracing=True
        )
