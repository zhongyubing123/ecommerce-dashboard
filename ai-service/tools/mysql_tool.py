import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        charset="utf8mb4"
    )


def execute_query(sql):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    finally:
        conn.close()



if __name__ == "__main__":
    sql = """
    SELECT COUNT(*)
    FROM ods_user_behavior;
    """

    result = execute_query(sql)
    print(result)