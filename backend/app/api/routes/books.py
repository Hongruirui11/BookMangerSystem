from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="获取图书列表")
async def list_books():
    """第一阶段先返回教学用的内存数据，下一阶段替换为 Tortoise 查询。"""
    return {
        "items": [
            {"id": 1, "title": "百年孤独", "author": "加西亚·马尔克斯"},
            {"id": 2, "title": "海边的卡夫卡", "author": "村上春树"},
        ],
        "total": 2,
    }


@router.get("/search", summary="按书名或作者查询")
async def search_books(keyword: str = ""):
    return {"keyword": keyword, "items": [], "total": 0}

