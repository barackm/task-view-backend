from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path


@CrewBase
class TaskAssignerCrew:
    """Crew for matching tasks with qualified users"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    output_directory = Path("outputs")

    def __init__(self):
        self.output_directory.mkdir(exist_ok=True)

    @agent
    def task_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["task_analyzer"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def user_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["user_profiler"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def workload_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["workload_analyzer"],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_task"],
            agent=self.task_analyzer(),
            output_file=str(self.output_directory / "analyze_task_output.txt"),
        )

    @task
    def analyze_users(self) -> Task:

        return Task(
            config=self.tasks_config["analyze_users"],
            agent=self.user_profiler(),
            output_file=str(self.output_directory / "analyze_users_output.txt"),
        )

    @task
    def analyze_workload(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_workload"],
            agent=self.workload_analyzer(),
            output_file=str(self.output_directory / "analyze_workload_output.txt"),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TaskAssigner crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
