# Sprint 03：MySQL Tool

> Date：2026-07-17  
> Author：zhongyubing

---

# Sprint Goal

封装 MySQL 数据库访问能力，为 AI Data Analyst Agent 提供统一的数据查询工具（Tool），实现 Python 与 MySQL 数据库的连接，为后续 AI Tool Calling 做准备。

---

# Background

目前 AI 服务已经能够：

```
User
   │
FastAPI
   │
DeepSeek
```

但是，大模型无法直接访问数据库，因此需要开发数据库工具（MySQL Tool），让 AI 后续能够通过 Tool 获取真实业务数据。

升级后的架构：

```
User
   │
FastAPI
   │
DeepSeek
   │
MySQL Tool
   │
MySQL
```

---

# Project Structure

新增目录：

```text
ai-service
│
├── app.py
├── services
├── prompts
├── tools
│   └── mysql_tool.py
└── .env
```

---

# Environment Configuration

在 `.env` 中新增数据库配置：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=******
MYSQL_DATABASE=ecommerce
```

> 注意：
>
> `.env` 文件已加入 `.gitignore`，
> 不允许上传到 GitHub，避免数据库账号和 API Key 泄露。

---

# Dependency Installation

安装 PyMySQL：

```bash
python -m pip install pymysql
```

验证：

```bash
python -c "import pymysql; print(pymysql.__version__)"
```

---

# MySQL Tool Design

新增文件：

```text
ai-service/tools/mysql_tool.py
```

主要功能：

## 1. get_connection()

负责创建数据库连接。

职责：

- 读取 `.env`
- 创建 MySQL 连接
- 返回 Connection 对象

---

## 2. execute_query(sql)

负责执行 SQL。

职责：

- 接收 SQL
- 执行查询
- 返回查询结果
- 自动关闭数据库连接

统一封装数据库访问逻辑，避免重复编写连接代码，提高代码复用性。

---

# Test

测试代码：

```python
if __name__ == "__main__":
    sql = "SELECT COUNT(*) FROM ods_user_behavior;"
    result = execute_query(sql)
    print(result)
```

运行：

```bash
python tools/mysql_tool.py
```

运行结果：

```text
((69555,),)
```

说明：

- MySQL 连接成功
- SQL 执行成功
- Tool 可以正常工作

---

# Development Summary

本 Sprint 完成内容：

- [x] 创建 tools 目录
- [x] 创建 mysql_tool.py
- [x] 配置 MySQL 环境变量
- [x] 封装数据库连接
- [x] 封装 SQL 查询函数
- [x] 完成数据库连接测试

---

# Technical Stack

- Python 3.11
- FastAPI
- PyMySQL
- python-dotenv
- MySQL

---

# Architecture

当前 AI 服务架构：

```
               User
                 │
                 ▼
             FastAPI
                 │
                 ▼
          DeepSeek Service
                 │
                 ▼
            MySQL Tool
                 │
                 ▼
               MySQL
```

---

# Key Learning

本阶段主要学习内容：

- 使用 PyMySQL 连接 MySQL
- 使用 `.env` 管理数据库配置
- 使用 `python-dotenv` 加载环境变量
- 封装数据库工具（Tool）
- 理解 AI Agent 中 Tool 的作用

---

# Next Sprint

Sprint 04：AI 调用数据库（Tool Calling）

目标：

```
User
   │
FastAPI
   │
DeepSeek
   │
MySQL Tool
   │
MySQL
   │
Database Result
   │
DeepSeek Analysis
   │
User
```

实现 AI 基于真实数据库查询结果进行数据分析，为后续 Function Calling 和 NL2SQL 打下基础。

---

# Git Commit

建议提交信息：

```bash
git add .

git commit -m "feat: add MySQL tool for AI agent"

git push
```

---

# Sprint Status

✅ Sprint 03 Completed