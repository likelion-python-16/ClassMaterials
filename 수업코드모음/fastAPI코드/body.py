# 추가적인 설명(제약, 메타데이터 등)을 붙이기 위한 기능
from typing import Annotated

# FastAPI 애플리케이션을 만들기 위한 메인 클래스로 반드시 있어야 FastAPI 서버를 만들 수 있어요 app = FastAPI()
from fastapi import Body, FastAPI

# Pydantic은 FastAPI에서 데이터를 검증하는 핵심 도구
from pydantic import BaseModel

app = FastAPI()

# 1. Pydantic 모델 정의
class Item(BaseModel): # 데이터 검증
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
# 클라이언트가 보낸 데이터에는 반드시 name(문자열)과 price(숫자)가 있어야 해! 라는 걸 뜻해요.  
# → 이걸 보고 FastAPI는 자동으로 유효성 검사를 해줘요.

class User(BaseModel): # 데이터 검증
    username: str
    full_name: str | None = None

# 2. PUT 메서드: item_id는 URL 경로에서, 나머지는 body에서 받음
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body()]
):
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    return results