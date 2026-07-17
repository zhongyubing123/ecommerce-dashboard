# Sprint 02：Prompt Engineering（提示词工程）

## 项目名称

AI Data Analyst Agent

---

## Sprint 信息

| 项目 | 内容 |
|------|------|
| Sprint | Sprint 02 |
| 开发时间 | 2026-07 |
| 开发阶段 | Prompt Engineering |
| 开发语言 | Python |
| 框架 | FastAPI |
| 大模型 | DeepSeek Chat |

---

# 一、开发目标

在 Sprint01 中，项目已经完成了 FastAPI 与 DeepSeek API 的集成，实现了基本的 AI 对话能力。

但是，此时的大模型仍然属于通用聊天机器人，不具备固定身份，也不能按照企业业务场景回答问题。

因此，本阶段需要引入 Prompt Engineering（提示词工程），为 AI 设置固定角色，使其成为一名专业的电商数据分析助手，为后续 Tool Calling、RAG、Memory 等功能奠定基础。

---

# 二、项目结构

本 Sprint 完成后的 AI 服务目录如下：

```text
ai-service
│
├── app.py
├── .env
├── requirements.txt
│
├── prompts
│   └── system_prompt.txt
│
└── services
    └── deepseek_service.py
```

新增目录：

```
prompts/
```

用于统一管理 Prompt。

---

# 三、为什么需要 Prompt？

默认情况下，大模型属于通用模型，例如：

用户：

```
为什么销量下降？
```

模型可能回答：

```
销量下降可能有很多原因，例如市场竞争、季节变化等……
```

这种回答虽然正确，但没有企业数据分析师的专业风格。

因此，需要增加 System Prompt，对模型进行角色约束。

---

# 四、System Prompt 设计

新增文件：

```
prompts/system_prompt.txt
```

内容如下：

```text
# Role

你是一名企业级 AI 数据分析助手。

## 你的职责

1. 回答有关电商数据分析的问题。
2. 帮助分析销量、品牌、商品、用户行为。
3. 不编造数据库中的数据。
4. 如果没有真实数据，明确告诉用户需要查询数据库。
5. 输出尽量专业、清晰、有条理。

## 输出格式

【分析】

......

【原因】

......

【建议】

......

## 注意

不要随意编造统计结果。

如果问题需要数据库数据，请说明：

"该问题需要查询数据库才能得到准确答案。"
```

---

# 五、为什么把 Prompt 独立出来？

企业开发一般不会把 Prompt 写死在 Python 代码中。

例如：

```python
system_prompt = """
xxxx
"""
```

虽然能够运行，但是存在以下问题：

- Prompt 修改需要重新部署程序
- Prompt 过长导致代码可读性下降
- 产品经理无法独立维护 Prompt

因此，本项目采用：

```
Prompt
↓

TXT 文件

↓

Python 动态读取
```

这种方式更加符合企业开发规范。

---

# 六、Prompt 加载

在：

```
services/deepseek_service.py
```

中新增：

```python
from pathlib import Path

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()
```

这样程序启动时即可自动读取 Prompt。

---

# 七、调用 DeepSeek

原来的 messages：

```python
messages = [
    {
        "role": "user",
        "content": message
    }
]
```

升级为：

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": message
    }
]
```

其中：

System Message：

负责定义 AI 身份。

User Message：

负责传递用户问题。

---

# 八、整体调用流程

```text
用户输入

↓

FastAPI

↓

读取 Prompt

↓

DeepSeek API

↓

生成回答

↓

返回用户
```

流程图：

```text
┌────────────┐
│    User    │
└─────┬──────┘
      │
      ▼
┌────────────┐
│  FastAPI   │
└─────┬──────┘
      │
      ▼
┌────────────────────┐
│ System Prompt      │
│ (system_prompt.txt)│
└─────┬──────────────┘
      │
      ▼
┌────────────┐
│ DeepSeek   │
└─────┬──────┘
      │
      ▼
┌────────────┐
│ AI Response│
└────────────┘
```

---

# 九、测试

启动项目：

```bash
uvicorn app:app --reload
```

访问：

```
http://127.0.0.1:8000/docs
```

调用：

```
POST /chat
```

输入：

```json
{
    "message":"为什么品牌销量下降？"
}
```

测试结果：

AI 能够按照 Prompt 设定，以专业数据分析师身份回答问题，并采用：

```
分析

原因

建议
```

三段式输出。

---

# 十、本 Sprint 遇到的问题

## 1、FastAPI 无法启动

错误：

```
Could not import module "app"
```

原因：

启动目录错误。

解决方案：

进入：

```
ai-service
```

目录后执行：

```bash
uvicorn app:app --reload
```

---

## 2、ImportError

错误：

```
from services.deepseek_service import chat
```

原因：

修改 Prompt 时误覆盖了 deepseek_service.py 文件，导致 chat() 方法丢失。

解决方案：

恢复 chat() 方法，并增加 Prompt 加载逻辑。

---

## 3、GitHub Push Protection

错误：

```
Push cannot contain secrets
```

原因：

DeepSeek API Key 被提交到了 Git。

解决方案：

- 使用 .gitignore 忽略 .env
- 删除 Git 中的 API Key
- 重新提交
- Push 成功

---

# 十一、本 Sprint 收获

完成了 Prompt Engineering 的基础能力。

掌握了：

✅ FastAPI

✅ DeepSeek API

✅ System Prompt

✅ Prompt 外置管理

✅ Path 文件读取

✅ OpenAI Messages 结构

✅ GitHub Secret Protection

---

