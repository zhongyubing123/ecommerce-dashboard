# Sprint 01：FastAPI + DeepSeek

> Date：2026-07-16
> Author：zhongyubing

---

# Sprint Goal

搭建 AI 服务基础框架，实现 FastAPI 与 DeepSeek API 的连接，完成第一个可调用的大语言模型接口，为后续 AI Agent 开发打下基础。

---

# Background

项目目标是开发一个 **AI Data Analyst Agent**，能够基于自然语言完成电商数据分析。

本阶段首先完成 AI 服务框架搭建，使客户端能够通过 HTTP 接口与 DeepSeek 大模型进行通信。

---

# Project Structure

创建项目目录：

```text
ecommerce/
│
├── ai-service/
│   ├── app.py
│   ├── services/
│   ├── prompts/
│   ├── .env
│   └── requirements.txt
│
├── backend/
└── vue/
```

---

# Environment

创建 Conda 环境：

```bash
conda create -n ai-agent python=3.11

conda activate ai-agent
```

安装依赖：

```bash
pip install fastapi uvicorn openai python-dotenv
```

---

# Environment Variables

创建：

```text
ai-service/.env
```

配置：

```env
DEEPSEEK_API_KEY=**************
```

> 注意：
>
> `.env` 已加入 `.gitignore`，
> 不上传 GitHub，防止 API Key 泄露。

---

# FastAPI

创建：

```text
app.py
```

实现：

- 创建 FastAPI 服务
- 创建 `/chat`
- 接收用户消息
- 返回 AI 回复

接口：

```http
POST /chat
```

请求：

```json
{
    "message":"你好"
}
```

返回：

```json
{
    "answer":"你好，我是 AI 数据分析助手。"
}
```

---

# DeepSeek Service

创建：

```text
services/
    deepseek_service.py
```

职责：

- 读取 API Key
- 创建 OpenAI Client
- 调用 DeepSeek Chat API
- 返回模型回复

统一封装模型调用逻辑。

---

# Running

启动：

```bash
uvicorn app:app --reload
```

访问：

```
http://127.0.0.1:8000/docs
```

Swagger 页面成功打开。

测试：

```
POST /chat
```

成功返回 DeepSeek 回复。

---

# Architecture

第一阶段整体架构：

```
User
   │
HTTP
   │
FastAPI
   │
DeepSeek API
   │
DeepSeek Model
```

---

# Development Summary

完成内容：

- [x] 创建 AI Service
- [x] 创建 FastAPI
- [x] 创建 Chat API
- [x] 接入 DeepSeek
- [x] 配置 .env
- [x] Swagger 测试成功

---

# Technical Stack

- Python 3.11
- FastAPI
- Uvicorn
- OpenAI SDK
- DeepSeek API
- python-dotenv

---

# Key Learning

本阶段学习内容：

- FastAPI 基础开发
- RESTful API
- OpenAI SDK 使用
- DeepSeek API 调用
- 环境变量管理（.env）
- Swagger 接口测试

---

# Next Sprint

Sprint 02：Prompt Engineering

目标：

- Prompt 文件独立管理
- System Prompt 加载
- Prompt 与代码解耦
- 提升 AI 回答稳定性

---

# Git Commit

建议提交：

```bash
git add .

git commit -m "feat: initialize FastAPI and DeepSeek service"

git push
```

---

# Sprint Status

✅ Sprint 01 Completed