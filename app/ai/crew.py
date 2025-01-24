from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Dict, List
from app.models.request_models import TaskAssigneeMatchResponse, UserSuggestion
import json


@CrewBase
class TaskAssignerCrew:
    """Crew for matching tasks with qualified users"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        # Initialize analysis results
        self.task_analysis = None
        self.user_analysis = None
        self.workload_analysis = None
        # Initialize contexts as lists
        self.task_context = []
        self.user_context = []
        self.workload_context = []
        self._inputs = None

    def set_contexts(self, inputs: Dict):
        """Set up contexts for all tasks"""
        print("\n=== Crew Input Data ===")
        print(f"Task Data: {json.dumps(inputs['task_data'], indent=2)}")
        print(f"Users: {json.dumps(inputs['users'], indent=2)}")
        print("=====================\n")

        self._inputs = inputs
        task_data = inputs["task_data"]
        users = inputs["users"]

        # Set task context
        self.task_context = [
            "You must analyze only the following task:",
            f"Title: {task_data['title']}",
            f"Description: {task_data['description']}",
            f"Priority: {task_data['priority']}",
            "Identify required skills and expertise level from the task description.",
            "Your output should be in JSON format.",
        ]
        print("\n=== Task Context ===")
        print("\n".join(self.task_context))
        print("==================\n")

        # Set user context
        self.user_context = [
            "Analyze only these actual users:",
            *[
                f"User ID: {user['id']}\nName: {user['full_name']}\nSkills: {', '.join(user['skills'])}\nCurrent Tasks: {len(user['tasks'])}"
                for user in users
            ],
            "Based on the task analysis, determine which users are qualified.",
            "Your output must be in JSON format with qualified_users array containing user IDs and qualification reasons.",
        ]
        print("\n=== User Context ===")
        print("\n".join(self.user_context))
        print("==================\n")

        # Set workload context
        self.workload_context = [
            f"New Task Priority: {task_data['priority']}",
            "For each qualified user, analyze their current workload:",
            *[
                f"User {user['id']} current tasks: {len(user['tasks'])}"
                for user in users
            ],
            "Return JSON with recommended_users array containing: {id: user_id, reason: 'qualification and workload explanation'}",
        ]
        print("\n=== Workload Context ===")
        print("\n".join(self.workload_context))
        print("=====================\n")

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
            context=self.task_context,
        )

    @task
    def analyze_users(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_users"],
            agent=self.user_profiler(),
            context=self.user_context,
        )

    @task
    def analyze_workload(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_workload"],
            agent=self.workload_analyzer(),
            context=self.workload_context,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TaskAssigner crew"""
        crew_instance = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

        # Override the default output to force JSON response
        def process_output(output):
            try:
                if hasattr(output, "tasks_output"):
                    # Get the final analysis
                    final_analysis = output.tasks_output[-1].raw
                    # Extract user suggestions
                    suggestions = []
                    for user in self._inputs["users"]:
                        # Only include users that match the required skills
                        if any(
                            skill.lower() in final_analysis.lower()
                            for skill in user["skills"]
                        ):
                            suggestions.append(
                                {
                                    "id": user["id"],
                                    "reason": f"Matches required skills: {', '.join(user['skills'])}. Current workload: {len(user['tasks'])} tasks.",
                                }
                            )
                    return TaskAssigneeMatchResponse(suggestions=suggestions)
                return TaskAssigneeMatchResponse(suggestions=[])
            except Exception as e:
                print(f"Error processing output: {e}")
                return TaskAssigneeMatchResponse(suggestions=[])

        crew_instance.process_output = process_output
        return crew_instance
