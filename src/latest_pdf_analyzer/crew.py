import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Process
from crewai.project import CrewBase, agent, task, crew

load_dotenv()

llm = LLM(
    model=os.getenv("MODEL"),  # groq/llama-3.1-70b-versatile
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
            llm=llm,
            verbose=True
        )

    @agent
    def hr_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_evaluator"],
            llm=llm,
            verbose=True
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

    @task
    def rewrite_resume(self) -> Task:
        return Task(
            config=self.tasks_config["rewrite_resume"],
            agent=self.resume_analyst(),
            context=[self.analyze_resume()]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.resume_analyst(),
                self.hr_evaluator()
            ],
            tasks=[
                self.analyze_resume(),
                self.evaluate_resume(),
                self.rewrite_resume()
            ],
            process=Process.sequential,
            verbose=True
        )
