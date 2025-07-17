from fastapi import FastAPI
from pydantic import BaseModel

fake_items_db = []

# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

# 아이템 생성
@app.post("/items/")
async def create_item(item: Item):
    fake_items_db.append(item)
    return item

# 전체 아이템 조회
@app.get("/items/")
async def read_item_list(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# 개별 아이템 조회
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return fake_items_db[item_id-1]

# 아이템 수정
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    fake_items_db[item_id-1] = item
    return fake_items_db[item_id-1]

# 아이템 삭제
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    fake_items_db.remove(fake_items_db[item_id-1])
    return {item_id: item_id}
