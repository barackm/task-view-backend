from typing import List
import logging
from app.config.supabase_client import supabase
from app.models.db_models import DBTask

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class DatabaseService:
    @staticmethod
    async def get_all_tasks() -> List[DBTask]:
        try:
            result = await supabase.table("tasks").select("*").execute()
            if not result.data:
                return []
            return [DBTask(**task) for task in result.data]

        except Exception as e:
            logger.error(f"Error getting all tasks: {e}")
            raise
