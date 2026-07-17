# Sprint 04：Agent Tool Calling V1

> Date：2026-07-17  
> Author：zhongyubing

---

# Sprint Goal

引入 Agent（智能决策层），实现 AI Service 与 MySQL Tool 的协同工作，使 AI 能够基于真实数据库查询结果进行数据分析，而不是仅依赖大模型自身知识。

---

# Background

前三个 Sprint 已完成：

- Sprint01：FastAPI 服务搭建
- Sprint02：Prompt Engineering
- Sprint03：MySQL Tool

目前系统已经能够：

```
User
   │
FastAPI
   │
DeepSeek
```

以及：

```
Python
   │
MySQL Tool
   │
MySQL
```

但是，这两个模块仍然是独立的。

本 Sprint 的目标是增加 Agent，使 AI 能够结合数据库查询结果回答用户问题。

---

# Project Architecture

新增 Agent 后：

```
                User
                  │
                  ▼
              FastAPI
                  │
                  ▼
            Agent Service
          ┌────────┴────────┐
          ▼                 ▼
   MySQL Tool        DeepSeek Service
          │                 ▲
          ▼                 │
        MySQL         Database Result
```

Agent 负责协调各个模块：

- 判断是否需要查询数据库
- 调用 MySQL Tool
- 获取数据库结果
- 将结果交给 DeepSeek 分析
- 返回最终答案

---

# Project Structure

新增：

```text
ai-service
│
├── app.py
├── prompts
├── services
│     ├── deepseek_service.py
│     └── agent_service.py
│
├── tools
│     └── mysql_tool.py
```

---

# Agent Design

新增：

```text
services/agent_service.py
```

职责：

- 接收用户问题
- 调用数据库工具
- 获取查询结果
- 调用 DeepSeek
- 返回最终回答

实现业务逻辑与 HTTP 接口分离，提高项目可维护性。

---

# Data Flow

执行流程：

```
用户输入

↓

FastAPI

↓

Agent Service

↓

MySQL Tool

↓

MySQL

↓

查询结果

↓

DeepSeek

↓

自然语言分析

↓

返回用户
```

---

# Development

本 Sprint 完成：

## 1. 创建 Agent Service

新增：

```text
services/agent_service.py
```

用于统一管理 AI Agent 的业务流程。

---

## 2. 调用 MySQL Tool

Agent 调用：

```
execute_query(sql)
```

获取数据库真实数据。

---

## 3. 调用 DeepSeek

数据库查询结果作为上下文传递给 DeepSeek。

例如：

```
数据库结果：

Nike
23500

Apple
22000
```

AI 基于真实数据完成分析。

---

# Advantages

相比直接在 app.py 编写业务逻辑：

```
FastAPI

↓

Agent

↓

Tool

↓

LLM
```

具有以下优势：

- 模块职责清晰
- 方便增加更多 Tool
- 易于维护
- 更符合企业 AI Agent 项目架构

---

# Development Summary

本 Sprint 完成：

- [x] 新增 Agent Service
- [x] Agent 调用 MySQL Tool
- [x] 数据库结果传递给 DeepSeek
- [x] AI 基于真实数据回答问题

---

# Technical Stack

- Python 3.11
- FastAPI
- DeepSeek API
- PyMySQL
- python-dotenv

---

# Architecture Evolution

Sprint01：

```
User
 │
 ▼
FastAPI
 │
 ▼
DeepSeek
```

Sprint03：

```
DeepSeek

MySQL Tool
```

Sprint04：

```
User
 │
 ▼
FastAPI
 │
 ▼
Agent
 │
 ├──────► MySQL Tool
 │            │
 │            ▼
 │         MySQL
 │
 ▼
DeepSeek
 │
 ▼
Answer
```

---

# Key Learning

本 Sprint 学习内容：

- 理解 Agent 的职责
- 理解 Tool 的作用
- 理解 AI Agent 架构
- 学习模块化设计思想
- 理解 AI 与数据库协同工作流程

---

# Next Sprint

Sprint05：Function Calling

目标：

实现真正的大模型 Tool Calling，让 AI 自主决定是否调用数据库，而不是依赖 Python 的固定逻辑。

最终架构：

```
User

↓

DeepSeek

↓

Function Calling

↓

MySQL Tool

↓

Database

↓

DeepSeek

↓

Answer
```

---

# Git Commit

建议提交：

```bash
git add .

git commit -m "feat: implement agent service and tool calling workflow"

git push
```

---

# Sprint Status

✅ Sprint 04 Completed