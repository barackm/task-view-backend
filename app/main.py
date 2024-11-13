from fastapi import FastAPI
from .modules.projects.route import router as projects_router
from .middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="My Project API",
    description="An API for task management using AI agents and Google sign-in",
    version="1.0.0",
)


app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.add_middleware(AuthMiddleware)

@app.get("/")
async def root():
    return {"message": "Welcome to My Project API!"}
