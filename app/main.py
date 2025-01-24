from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.request_models import (
    TaskAssigneeMatchRequest,
    TaskAssigneeMatchResponse,
)
from app.ai.crew import TaskAssignerCrew
import uvicorn

app = FastAPI(
    title="Task Management API",
    description="An API for task management using AI agents",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Task Management API!"}


@app.post("/assignee-candidates", response_model=TaskAssigneeMatchResponse)
async def assignee_candidates(request: TaskAssigneeMatchRequest):
    try:
        print("\n=== Input Data ===")
        print("\nTask Data:")
        print(f"Title: {request.task_data.title}")
        print(f"Description: {request.task_data.description}")
        print(f"Priority: {request.task_data.priority}")

        print("\nUsers:")
        for user in request.users:
            print(f"\nUser ID: {user.id}")
            print(f"Name: {user.full_name}")
            print(f"Skills: {', '.join(user.skills)}")
            print("Tasks:", [f"{t.title} ({t.priority})" for t in user.tasks])
        print("\n================\n")

        inputs = {
            "task_data": request.task_data.model_dump(),
            "users": [user.model_dump() for user in request.users],
        }

        crewClass = TaskAssignerCrew()
        result = crewClass.crew().kickoff(inputs=inputs)
        print(result)
        return result
    except Exception as e:
        print(f"Error in assignee_candidates: {e}")
        return TaskAssigneeMatchResponse(suggestions=[])


def start():
    """Entry point for the application."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
