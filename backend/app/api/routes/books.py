from fastapi import APIRouter, HTTPException, Query, status
from tortoise.expressions import Q

from app.models.book import Book
from app.schemas.book import BookCreate, BookListResponse, BookResponse, BookUpdate

router = APIRouter()


@router.get("/", response_model=BookListResponse, summary="获取图书列表")
async def list_books():
    books = await Book.all().order_by("-created_at")
    return {"items": books, "total": len(books)}


@router.get("/search", response_model=BookListResponse, summary="按书名或作者查询")
async def search_books(keyword: str = Query(default="", max_length=100)):
    query = Book.all()
    if keyword.strip():
        text = keyword.strip()
        query = query.filter(Q(title__icontains=text) | Q(author__icontains=text))
    books = await query.order_by("-created_at")
    return {"items": books, "total": len(books)}


@router.get("/{book_id}", response_model=BookResponse, summary="获取图书详情")
async def get_book(book_id: int):
    book = await Book.get_or_none(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    return book


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="新增图书")
async def create_book(payload: BookCreate):
    return await Book.create(**payload.model_dump())


@router.put("/{book_id}", response_model=BookResponse, summary="编辑图书")
async def update_book(book_id: int, payload: BookUpdate):
    book = await Book.get_or_none(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    book.update_from_dict(payload.model_dump())
    await book.save()
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除图书")
async def delete_book(book_id: int):
    book = await Book.get_or_none(id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="图书不存在")
    await book.delete()
