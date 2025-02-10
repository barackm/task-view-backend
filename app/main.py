from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.request_models import (
    TaskAssigneeMatchRequest,
    TaskAssigneeMatchResponse,
    TaskDescriptionRequest,
    TaskDescriptionResponse,
    TaskDurationRequest,
    TaskDurationResponse,
)
from app.ai.crew import TaskAssignerCrew
from typing import Optional
from pydantic import BaseModel
import uvicorn
from app.ai.openai_client import get_task_description, get_task_duration
from app.services.db_service import DatabaseService

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
    all_tasks = await DatabaseService.get_all_tasks()
    return {"message": "Welcome to Task Management API!", "tasks": all_tasks}


@app.post("/assignee-candidates")
async def assignee_candidates(request: TaskAssigneeMatchRequest):
    try:
        inputs = {
            "task_data": request.task_data.model_dump(),
            "users": [user.model_dump() for user in request.users],
        }
        crewClass = TaskAssignerCrew()
        result = crewClass.crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        print(f"Error in assignee_candidates: {e}")
        return TaskAssigneeMatchResponse(suggestions=[])


class TextToSpeechRequest(BaseModel):
    filename: str
    voice: Optional[str] = "alloy"


@app.post("/suggest-description")
async def suggest_description(
    request: TaskDescriptionRequest,
) -> TaskDescriptionResponse:
    try:
        description = get_task_description(request.title)
        return TaskDescriptionResponse(description=description)
    except Exception as e:
        print(f"Error in suggest_description: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate task description"
        )


@app.post("/suggest-duration")
async def suggest_duration(
    request: TaskDurationRequest,
) -> TaskDurationResponse:
    try:
        assignee_dict = request.assignee.model_dump() if request.assignee else None
        duration, explanation = get_task_duration(
            request.title, request.description, assignee_dict
        )
        return TaskDurationResponse(duration=duration, explanation=explanation)
    except Exception as e:
        print(f"Error in suggest_duration: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to generate task duration estimate"
        )


def start():
    """Entry point for the application."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
