from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 간단한 메모리 기반 DB 역할을 하는 리스트
fake_items_db = []

# Pydantic 모델 정의 (요청 및 응답 구조)
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# FastAPI 앱 인스턴스 생성
app = FastAPI()


# ✅ CREATE: 아이템 생성
@app.post("/items/")
async def create_item(item: Item):
    """
    새 아이템을 생성하여 DB(fake_items_db)에 추가합니다.
    """
    fake_items_db.append(item)
    return item


# ✅ READ (전체 조회): 아이템 목록 조회 (페이징 지원)
@app.get("/items/")
async def read_item_list(skip: int = 0, limit: int = 10):
    """
    아이템 목록을 일부(skip부터 limit까지) 반환합니다.
    기본값은 처음 10개입니다.
    """
    return fake_items_db[skip: skip + limit]


# ✅ READ (단일 조회): 특정 아이템 조회
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    item_id에 해당하는 아이템 하나를 조회합니다.
    item_id는 1부터 시작한다고 가정합니다.
    """
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id - 1]


# ✅ UPDATE: 특정 아이템 수정
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    item_id에 해당하는 아이템을 새로운 값으로 수정합니다.
    """
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    fake_items_db[item_id - 1] = item
    return item


# ✅ DELETE: 특정 아이템 삭제
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """
    item_id에 해당하는 아이템을 목록에서 제거합니다.
    """
    if item_id <= 0 or item_id > len(fake_items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    removed_item = fake_items_db.pop(item_id - 1)
    return {"deleted_item": removed_item}

# ✅ IndexError 방지: item_id가 유효한 범위인지 검사하는 if문 추가
# ✅ pop()을 사용하여 삭제된 아이템을 반환
# ✅ BaseModel을 활용한 데이터 검증
# ✅ 전체 기능에 docstring 주석을 추가하여 Swagger 문서에도 자동 반영

