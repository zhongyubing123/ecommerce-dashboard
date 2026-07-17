from fastapi import FastAPI
from pydantic import BaseModel

from services.deepseek_service import chat
from tools.mysql_tool import execute_query

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat_api(req: ChatRequest):

    db_result = None

    # 如果用户问品牌相关问题，就查询数据库
    if "品牌" in req.message:

        sql = """
        SELECT brand,
               SUM(sales_amount) AS total_sales
        FROM dws_brand_sales
        GROUP BY brand
        ORDER BY total_sales DESC
        LIMIT 10;
        """

        db_result = execute_query(sql)

    answer = chat(req.message, db_result)

    return {
        "answer": answer
    }