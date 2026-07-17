import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


def chat(message, db_result=None):
   
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        if db_result is not None:
           messages.append(
            {
                "role": "system",
                "content": f"数据库查询结果：{db_result}"
            }
        )
        messages.append(
            {
                "role": "user",
                "content": message
            }
        )
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
        )

        return response.choices[0].message.content