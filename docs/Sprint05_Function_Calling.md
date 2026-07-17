# Sprint05 开发文档 —— Function Calling 与 MySQL Tool 调用

## 一、开发目标

本 Sprint 的目标是在 AI Agent 中实现 Function Calling（函数调用）机制，使大语言模型不仅能够进行自然语言对话，还能够根据用户的问题自动调用数据库查询工具，并结合查询结果生成最终回答。

---

## 二、实现目标

完成以下功能：

- 注册 MySQL 查询工具（Tool）
- DeepSeek 返回 Tool Call
- Python 解析 Tool Call
- 调用 MySQL 数据库
- 获取数据库查询结果
- 将查询结果返回给 DeepSeek
- DeepSeek 根据真实数据生成最终回答

实现 AI → Tool → Database → AI 的完整闭环。

---

## 三、系统流程

```text
                User
                  │
                  ▼
        DeepSeek（第一次请求）
                  │
                  ▼
          Function Calling
                  │
                  ▼
        Python Tool Executor
                  │
                  ▼
              MySQL Database
                  │
                  ▼
         查询结果(Result)
                  │
                  ▼
        DeepSeek（第二次请求）
                  │
                  ▼
             最终回答(User)
```

---

## 四、项目结构

```text
ai-service
│
├── app.py
│
├── services
│   └── deepseek_service.py
│
├── tools
│   └── mysql_tool.py
│
├── prompts
│   └── system_prompt.txt
│
└── .env
```

---

## 五、核心实现

### 1、注册 Tool

向 DeepSeek 注册 MySQL 查询工具。

```python
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
                        "type": "string"
                    }
                },
                "required": ["sql"]
            }
        }
    }
]
```

---

### 2、第一次调用 DeepSeek

发送用户问题，并允许模型调用工具。

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools
)
```

---

### 3、获取 Tool Call

解析模型返回的工具调用请求。

```python
assistant_message = response.choices[0].message

tool_call = assistant_message.tool_calls[0]
```

输出示例：

```text
工具名称：
query_mysql

工具参数：
{
    "sql":"SELECT ..."
}
```

---

### 4、执行数据库查询

当前 Sprint 为了验证 Function Calling 流程，采用固定 SQL。

```python
sql = """
SELECT
    brand,
    SUM(sales_amount) AS total_sales
FROM dws_brand_sales
GROUP BY brand
ORDER BY total_sales DESC
LIMIT 10;
"""

result = execute_query(sql)
```

数据库返回：

```text
[
    ('Apple', 853000.5),
    ('Huawei', 801234.8),
    ...
]
```

---

### 5、返回 Tool 结果

将数据库查询结果发送回 DeepSeek。

```python
messages.append(assistant_message)

messages.append(
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    }
)
```

---

### 6、第二次调用 DeepSeek

根据数据库查询结果生成最终回答。

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
```

最终返回：

```python
return response.choices[0].message.content
```

---

## 六、测试

### 测试一

输入：

```text
销量最高品牌有哪些？
```

AI 返回：

```text
我来查询数据库中销量最高的品牌。
```

随后调用：

```text
query_mysql()
```

数据库执行 SQL：

```sql
SELECT
brand,
SUM(sales_amount) AS total_sales
FROM dws_brand_sales
GROUP BY brand
ORDER BY total_sales DESC
LIMIT 10;
```

最终返回：

```text
销量最高的品牌为 XXX，
销售额为 XXXXX。
```

---

### 测试二

输入：

```text
你好
```

由于无需调用数据库：

```text
assistant_message.tool_calls == None
```

AI 直接回复普通聊天内容。

---

## 七、Sprint05 成果

本 Sprint 完成了 AI Agent 的 Function Calling 核心能力。

目前系统已经具备：

- DeepSeek Function Calling
- Tool 注册
- Tool Call 解析
- Python Tool Executor
- MySQL 查询
- 二次调用大模型
- 基于真实数据库结果生成回答

实现了完整的 AI 工具调用闭环。

---

## 八、存在的问题

当前版本为了验证 Function Calling 流程，数据库查询 SQL 采用固定写法：

```python
sql = """
SELECT ...
"""
```

AI 虽然能够生成 Tool Call，但生成的 SQL 并未真正执行。

下一阶段将升级为：

- 自动读取数据库 Schema
- DeepSeek 自动生成 SQL（NL2SQL）
- Python 执行 AI 生成的 SQL
- 返回真实查询结果

进一步实现企业级智能数据分析 Agent。

---

## 九、下一步计划（Sprint06）

下一 Sprint 将实现：

- 数据库 Schema 注入
- NL2SQL（自然语言生成 SQL）
- AI 自动执行 SQL
- 动态数据分析
- 多表联合查询
- 智能数据问答

最终实现真正的智能数据分析 Agent。

---

## 十、本 Sprint 总结

Sprint05 实现了 AI Agent 的 Function Calling 能力，使系统具备调用外部工具的能力，完成了从自然语言理解到数据库查询再到智能回答的完整流程，为后续 NL2SQL 和智能数据分析奠定了基础。