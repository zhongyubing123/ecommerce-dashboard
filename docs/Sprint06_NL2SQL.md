# Sprint06 开发文档 —— NL2SQL（Natural Language to SQL）

## 一、开发目标

本 Sprint 的目标是在 AI Agent 中实现自然语言生成 SQL（NL2SQL）能力，使大语言模型能够根据用户输入自动生成 SQL，并查询 MySQL 数据库返回结果。

相较于 Sprint05 中固定 SQL 查询，本 Sprint 将数据库结构（Schema）提供给大语言模型，使其能够根据数据库表结构动态生成 SQL，提高系统的智能化程度。

---

# 二、实现目标

完成以下功能：

- 注入数据库 Schema
- AI 自动理解数据库结构
- AI 自动生成 SQL
- Python 执行 AI 生成的 SQL
- MySQL 返回查询结果
- AI 根据查询结果生成最终回答
- SQL 异常捕获

---

# 三、系统流程

```text
             User
               │
               ▼
      DeepSeek（理解问题）
               │
               ▼
     根据 Schema 生成 SQL
               │
               ▼
      Python 获取 SQL
               │
               ▼
        MySQL Database
               │
               ▼
         查询结果(Result)
               │
               ▼
      DeepSeek（二次回答）
               │
               ▼
            Final Answer
```

---

# 四、项目结构

```text
ai-service
│
├── app.py
│
├── prompts
│   ├── system_prompt.txt
│   └── schema.txt
│
├── services
│   └── deepseek_service.py
│
├── tools
│   └── mysql_tool.py
│
└── .env
```

---

# 五、核心实现

## 1、数据库 Schema

新增：

```text
prompts/schema.txt
```

内容包含：

- 数据库名称
- 数据表名称
- 字段名称
- 字段说明

例如：

```text
Table: dws_brand_sales

Columns:
brand
sales_amount
buy_count
```

作用：

帮助 DeepSeek 理解数据库结构。

---

## 2、读取 Schema

在 deepseek_service.py 中读取 schema.txt。

```python
SCHEMA_PATH = Path(__file__).parent.parent / "prompts" / "schema.txt"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    SCHEMA = f.read()
```

---

## 3、注入 Prompt

将 System Prompt 与数据库 Schema 合并发送给 DeepSeek。

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT + "\n\n" + SCHEMA
    }
]
```

这样模型可以知道数据库中有哪些表和字段。

---

## 4、AI 自动生成 SQL

注册 Tool：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_mysql",
            ...
        }
    }
]
```

模型返回：

```json
{
    "sql":
    "SELECT brand,
     SUM(sales_amount)
     FROM dws_brand_sales
     GROUP BY brand"
}
```

解析：

```python
args = json.loads(tool_call.function.arguments)

sql = args["sql"]
```

---

## 5、执行 SQL

Python 调用数据库工具：

```python
result = execute_query(sql)
```

打印日志：

```python
print(sql)

print(result)
```

---

## 6、SQL 异常处理

增加异常捕获：

```python
try:
    result = execute_query(sql)

except Exception as e:
    return f"数据库查询失败：{e}"
```

避免 SQL 出错导致 FastAPI 返回 500。

---

# 六、测试

## 测试一

输入：

```text
销量最高品牌有哪些？
```

AI 自动生成：

```sql
SELECT
brand,
SUM(sales_amount)
FROM dws_brand_sales
GROUP BY brand
ORDER BY sales_amount DESC;
```

返回：

品牌销量排行榜。

---

## 测试二

输入：

```text
销量最高商品类别？
```

生成：

```sql
SELECT *
FROM dws_category_sales
ORDER BY sales_amount DESC
LIMIT 1;
```

查询成功。

---

## 测试三

输入：

```text
购买次数最多的用户？
```

生成：

```sql
SELECT
user_id,
buy_count
FROM dws_user_active
ORDER BY buy_count DESC
LIMIT 1;
```

返回用户信息。

---

## 测试四

输入：

```text
销量最高商品？
```

由于 Schema 中表名与数据库实际表名不一致，AI 生成：

```sql
FROM dws_hot_items
```

数据库返回：

```text
Table doesn't exist
```

修正 Schema 后恢复正常。

---

# 七、Sprint06 成果

本 Sprint 完成了 AI Agent 的 NL2SQL 核心能力。

系统已经具备：

- 数据库 Schema 理解
- AI 自动生成 SQL
- 动态执行 SQL
- MySQL 查询
- AI 根据数据库结果回答
- SQL 异常处理

实现了自然语言到数据库查询的完整流程。

---

# 八、存在的问题

当前系统仅支持一次 Tool Calling。

当 AI 希望连续查询多张数据表时，程序不会继续执行第二次 Tool Call。

例如：

```text
查询用户购买记录

↓

查询品牌信息

↓

查询商品信息
```

目前仅执行第一次查询。

下一 Sprint 将升级为 Multi-step Agent，实现多轮 Tool Calling。

---

# 九、下一步计划（Sprint07）

下一 Sprint 将实现：

- Multi-step Agent
- 多轮 Tool Calling
- 自动循环调用工具
- 多表联合分析
- 更复杂的数据分析能力

进一步提升 AI Agent 的智能分析能力。

---

# 十、本 Sprint 总结

Sprint06 实现了 AI Agent 的自然语言生成 SQL（NL2SQL）能力，使系统能够理解数据库结构，根据用户问题动态生成 SQL 并完成查询，显著提升了系统的智能化水平，为后续多轮工具调用和复杂数据分析奠定了基础。