import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def chat(message: str):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一名AI数据分析助手，擅长电商数据分析。"
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content