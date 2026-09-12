from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from app.api.routes.books import router as books_router
from app.db import TORTOISE_ORM

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="教学型图书管理系统", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(books_router, prefix="/api/books", tags=["图书"])
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=True)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"title": "图书管理系统", "api_docs": "/docs"},
    )


@app.get("/health", tags=["系统"])
async def health_check():
    return {"status": "ok", "message": "FastAPI 服务运行中"}


@app.get("/api/request-demo", tags=["教学示例"])
async def request_demo(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "client": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
    }
