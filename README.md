# 教学型图书管理系统

一个用于学习 FastAPI 的前后端分离示例项目。

## 当前技术栈

- 前端：Vue 3 + Vite
- 后端：FastAPI
- ORM：Tortoise-ORM（下一阶段接入）
- 数据库：MySQL（下一阶段接入）

## 目录

```text
backend/    FastAPI 后端
frontend/   Vue 3 + Vite 前端
docs/       设计文档和实现计划
```

## 启动后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开 <http://127.0.0.1:8000/docs> 查看自动生成的 API 文档，打开 <http://127.0.0.1:8000/> 查看模板示例。

## 启动前端

```bash
cd frontend
npm install
npm run dev
```

MySQL 连接配置和 CRUD 说明将在后续阶段补充。

