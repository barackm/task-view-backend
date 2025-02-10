from typing import List
import logging
from app.config.supabase_client import supabase
from app.models.db_models import DBTask, DBProject, DBProfile

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class DatabaseService:
    @staticmethod
    def _parse_skills(skills: str | None) -> List[str]:
        """Convert comma-separated skills string to list"""
        if not skills:
            return []
        return [skill.strip() for skill in skills.split(",")]

    @staticmethod
    async def get_all_tasks() -> List[DBTask]:
        try:
            result = supabase.table("tasks").select("*").execute()
            if not result.data:
                return []
            return [DBTask(**task) for task in result.data]
        except Exception as e:
            logger.error(f"Error getting all tasks: {e}")
            raise

    @staticmethod
    async def get_all_profiles() -> List[DBProfile]:
        try:
            result = supabase.table("profiles").select("*").execute()
            if not result.data:
                return []

            profiles = []
            for profile in result.data:
                # Convert skills string to list before creating DBProfile
                profile["skills"] = DatabaseService._parse_skills(profile.get("skills"))
                profiles.append(DBProfile(**profile))
            return profiles

        except Exception as e:
            logger.error(f"Error getting all profiles: {e}")
            raise

    @staticmethod
    async def get_task_by_id(task_id: str) -> DBTask:
        try:
            result = supabase.table("tasks").select("*").eq("id", task_id).execute()
            return DBTask(**result.data[0])
        except Exception as e:
            logger.error(f"Error getting task by id: {e}")
            raise

    @staticmethod
    async def get_project_by_id(project_id: str) -> DBProject:
        try:
            result = (
                supabase.table("projects").select("*").eq("id", project_id).execute()
            )
            return DBProject(**result.data[0])
        except Exception as e:
            logger.error(f"Error getting project by id: {e}")
            raise
