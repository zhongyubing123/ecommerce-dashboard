import os
from pathlib import Path
import json
from dotenv import load_dotenv
from openai import OpenAI

from tools.mysql_tool import execute_query

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

SCHEMA_PATH = Path(__file__).parent.parent / "prompts" / "schema.txt"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = f.read()

def chat(message, db_result=None):
    """
    AI 对话服务（Sprint05）
    功能：
    1. 注册 MySQL Tool
    2. 接收 Function Calling
    3. 调用 MySQL
    4. 将数据库结果返回给 DeepSeek
    """

    # ==========================
    # 组织消息
    # ==========================
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT+ "\n\n" + SCHEMA
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

    # ==========================
    # 注册工具
    # ==========================
    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_mysql",
                "description": "Query sales data from MySQL database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL statement"
                        }
                    },
                    "required": ["sql"]
                }
            }
        }
    ]

    # ==========================
    # 第一次调用 DeepSeek
    # ==========================
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )

    assistant_message = response.choices[0].message

    print("========== LLM 返回 ==========")
    print(assistant_message)

    # ==========================
    # 没有 Tool Call
    # ==========================
    if not assistant_message.tool_calls:
        return assistant_message.content

    # ==========================
    # 解析 Tool Call
    # ==========================
    tool_call = assistant_message.tool_calls[0]

    print("工具名称：", tool_call.function.name)
    print("工具参数：", tool_call.function.arguments)

    result = None

    if tool_call.function.name == "query_mysql":

    # 解析 AI 返回的参数
       args = json.loads(tool_call.function.arguments)

    # 获取 AI 生成的 SQL
       sql = args["sql"]

       print("========== AI 生成的 SQL ==========")
       print(sql)

    try:
        result = execute_query(sql)

        print("========== 数据库查询结果 ==========")
        print(result)

    except Exception as e:

        print("========== SQL 执行失败 ==========")
        print(e)

        return f"数据库查询失败：{e}"
     
    # ==========================
    # 将 Tool 结果返回给 DeepSeek
    # ==========================
    messages.append(assistant_message)

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        }
    )

    # ==========================
    # 第二次调用 DeepSeek
    # ==========================
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    final_answer = response.choices[0].message.content

    print("========== AI 最终回答 ==========")
    print(final_answer)

    return final_answer