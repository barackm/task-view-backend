from fastapi import FastAPI
from .modules.projects.route import router as projects_router
from .modules.tasks.route import router as tasks_router
from .modules.comments.route import router as comments_router
from .auth.route import router as auth_router
from .modules.users.route import router as users_router

from .middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="Task Management API",
    description="An API for task management using AI agents",
    version="1.0.0",
)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])

app.add_middleware(AuthMiddleware, exempt_routes=["/auth/signup", "/auth/login", "/docs", "/"])

@app.get("/")
async def root():
    return {"message": "Welcome to My Project API!"}

