from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class TaskViewManagerCrew:
    """TaskViewManager Crew for task assignment."""
    
    def __init__(self, task_data=None, users=None):
        """Initialize the crew with task data and users."""
        self.agents_config = 'config/agents.yaml'
        self.tasks_config = 'config/tasks.yaml'
        self.task_data = task_data
        self.users = users
    
    @agent
    def domain_classifier(self) -> Agent:
        """Agent responsible for classifying task and user domains."""
        return Agent(
            role="Domain Classification Expert",
            goal="Accurately classify tasks and users into their respective domains",
            backstory="I am an expert at identifying which domain a task or person belongs to",
            verbose=True,
            allow_delegation=False
        )
    
    @agent
    def task_matcher(self) -> Agent:
        """Agent responsible for analyzing and suggesting task assignments."""
        return Agent(
            config=self.agents_config['task_matcher_agent'],
            allow_delegation=False,
            verbose=True,
            context={
                'task_data': self.task_data,
                'users': self.users
            }
        )
        
    @task
    def classify_domains_task(self) -> Task:
        """Task for classifying domains of task and users."""
        return Task(
            config=self.tasks_config['classify_domains_task'],
            agent=self.domain_classifier()
        )
        
    @task
    def analyze_assignment_task(self) -> Task:
        """Task for analyzing and suggesting assignments."""
        return Task(
            config=self.tasks_config['analyze_and_assign_task'],
            agent=self.task_matcher(),
            context=[self.classify_domains_task()]  # Use results from classification
        ) 
        
    @crew
    def crew(self) -> Crew:
        """Creates the TaskViewManager Crew."""
        return Crew(
            agents=[self.domain_classifier(), self.task_matcher()],
            tasks=[self.classify_domains_task(), self.analyze_assignment_task()],
            process=Process.sequential,
            verbose=True
        )