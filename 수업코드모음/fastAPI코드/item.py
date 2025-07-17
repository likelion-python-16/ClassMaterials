from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 요청 및 응답으로 사용할 모델 정의
class Item(BaseModel):
    name: str
    description: str | None = None  # 필수가 아님
    price: float
    tax: float | None = None        # 필수가 아님

# POST 요청 처리
@app.post("/items/")
async def create_item(item: Item):
    return {
        "message": "Item received successfully!",
        "item_data": item
    }