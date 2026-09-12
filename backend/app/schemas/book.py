from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    isbn: str | None = Field(default=None, max_length=20)
    publisher: str | None = Field(default=None, max_length=120)
    published_year: int | None = Field(default=None, ge=0, le=3000)
    description: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class BookListResponse(BaseModel):
    items: list[BookResponse]
    total: int

