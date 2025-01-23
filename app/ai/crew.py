from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

llm = LLM(
    model="gpt-4-1106-preview",  # Use proper OpenAI model name
    temperature=0.8,
    max_tokens=150,
    top_p=0.9,
    frequency_penalty=0.1,
    presence_penalty=0.1,
    stop=["END"],
    seed=42
)

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
            config=self.agents_config['domain_classifier_agent'],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    @agent
    def task_matcher(self) -> Agent:
        """Agent responsible for matching tasks with suitable users."""
        return Agent(
            config=self.agents_config['task_matcher_agent'],
            verbose=True,
            allow_delegation=False,
            llm=llm,
            context={
                'task_data': self.task_data,
                'users': self.users
            }
        )
        
    @task
    def classify_domains_task(self) -> Task:
        """Task for strict domain classification."""
        return Task(
            config=self.tasks_config['classify_domains_task'],
            agent=self.domain_classifier(),
            llm=llm
        )
        
    @task
    def analyze_assignment_task(self) -> Task:
        """Task for finding suitable assignees."""
        return Task(
            config=self.tasks_config['analyze_and_assign_task'],
            agent=self.task_matcher(),
            context=[self.classify_domains_task()],
            llm=llm
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