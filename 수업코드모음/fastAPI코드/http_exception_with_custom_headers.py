from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {    
	"apple": "사과입니다",
    "banana": "바나나입니다",
    "grape": "포도입니다"
    }

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        # 헤더를 직접 지정해서 반환할 수 있습니다.
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}