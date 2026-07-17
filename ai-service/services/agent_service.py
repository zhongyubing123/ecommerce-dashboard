from services.deepseek_service import chat
from tools.mysql_tool import execute_query


def run_agent(message: str):
    """
    AI Agent

    Args:
        message: 用户问题

    Returns:
        AI 回复
    """

    # 默认没有数据库结果
    db_result = None

    # 如果用户询问品牌销量
    if "品牌" in message and "销量" in message:

        sql = """
        SELECT brand, COUNT(*) AS sales
        FROM ods_user_behavior
        WHERE behavior='buy'
        GROUP BY brand
        ORDER BY sales DESC
        LIMIT 5;
        """

        db_result = execute_query(sql)

    # 调用 DeepSeek
    answer = chat(message, db_result)

    return answer