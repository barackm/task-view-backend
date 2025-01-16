from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class TaskViewManagerCrew:
    """TaskViewManager Crew for managing tasks."""
    
    def __init__(self, db):
        """Initialize the crew with the database session."""
        self.agents_config = 'config/agents.yaml'
        self.tasks_config = 'config/tasks.yaml'
    
    @agent
    def task_matcher(self) -> Agent:
        """Agent responsible for matching tasks to the most suitable team members."""
        return Agent(
            config=self.agents_config['task_matcher_agent'],
            allow_delegation=False,
            verbose=True,
        )
        
    @task
    def match_tasks_task(self) -> Task:
        """Task for Task Matcher to assign tasks to suitable team members."""
        return Task(
            config=self.tasks_config['match_skills_to_task_task'],
            agent=self.task_matcher(),
        ) 
         
    @task
    def prioritize_task_assignments_task(self) -> Task:
        """Task to prioritize task assignments based on urgency and team availability."""
        return Task(
            config=self.tasks_config['prioritize_task_assignments_task'],
            agent=self.task_matcher(),
            context=[self.match_tasks_task()]
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the TaskViewManager Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )