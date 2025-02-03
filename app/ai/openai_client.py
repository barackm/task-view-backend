from openai import OpenAI
import os
from typing import Optional

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_task_description(title: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates detailed task descriptions. Include the main objective, key requirements, and expected outcome in 2-3 sentences.",
                },
                {
                    "role": "user",
                    "content": f"Create a detailed description for a task titled: {title}. Include what needs to be done, why it's important, and what the expected outcome is.",
                },
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting task description: {e}")
        return "Failed to generate description"


def get_task_duration(
    title: str, description: str, assignee: Optional[dict] = None
) -> tuple[str, str]:
    try:
        # Build user context if assignee is provided
        user_context = ""
        if assignee:
            user_context = f"\nAssignee Skills: {', '.join(assignee['skills'])}\nCurrent Tasks: {len(assignee['tasks'])}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are a project management assistant that estimates task durations.
                    Consider the assignee's skills and current workload when provided.
                    Always format duration as a number followed by either 'minutes', 'hours', or 'days'.
                    Examples of valid formats: '2 days', '4 hours', '30 minutes'.
                    Always respond with duration on first line, explanation on second line.
                    If the assignee has relevant skills, they might complete the task faster.""",
                },
                {
                    "role": "user",
                    "content": f"Suggest a duration for this task:\nTitle: {title}\nDescription: {description}{user_context}",
                },
            ],
            max_tokens=150,
            temperature=0.7,
        )
        content = response.choices[0].message.content.strip()

        # Split into duration and explanation
        parts = content.split("\n", 1)
        duration = parts[0].strip()
        explanation = parts[1].strip() if len(parts) > 1 else "No explanation provided"

        # Validate duration format
        import re

        if not re.match(r"^\d+\s+(minutes|hours|days)$", duration):
            return "4 hours", "Default estimate provided due to invalid format"

        return duration, explanation
    except Exception as e:
        print(f"Error getting task duration: {e}")
        return "4 hours", "Error occurred while generating estimate"
