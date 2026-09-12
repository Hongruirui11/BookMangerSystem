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

## MySQL 配置

先创建数据库（用户和权限可以按本机环境调整）：

```sql
CREATE DATABASE book_manager DEFAULT CHARACTER SET utf8mb4;
```

复制 `backend/.env.example` 为 `backend/.env`，填写 MySQL 账号密码。开发环境启动时 Tortoise-ORM 会自动创建表结构。

## 当前 API

- `GET /api/books/`：列表
- `GET /api/books/search?keyword=vue`：查询
- `GET /api/books/{id}`：详情
- `POST /api/books/`：新增
- `PUT /api/books/{id}`：编辑
- `DELETE /api/books/{id}`：删除
- `GET /api/request-demo`：Request 对象教学示例
