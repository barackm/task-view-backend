from fastapi import FastAPI

app = FastAPI(
    title="My Project API",
    description="An API for task management using AI agents and Google sign-in",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "Welcome to My Project API!"}
