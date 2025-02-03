from openai import OpenAI
import os

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
