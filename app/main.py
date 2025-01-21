from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.request_models import TaskAssigneeMatchRequest
from app.ai.crew import TaskViewManagerCrew
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


@app.post("/assignee-candidates")
async def assignee_candidates(request: TaskAssigneeMatchRequest):
    crew = TaskViewManagerCrew(
        task_data=request.task_data.model_dump(),
        users=[user.model_dump() for user in request.users]
    )
    result = crew.crew().kickoff()
    return result

def start():
    """Entry point for the application."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
