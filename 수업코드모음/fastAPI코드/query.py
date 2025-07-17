from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search")
async def search_items(
    q: Annotated[str, Query(min_length=3, max_length=50, description="검색 키워드")] = ...,
    limit: Annotated[int, Query(ge=1, le=100, description="최대 결과 수 (1~100)")] = 5,
    offset: Annotated[int, Query(ge=0, description="몇 번째 결과부터 시작할지")] = 0,
):
    dummy_data = [f"{q}_result_{i}" for i in range(1, 101)]

    return {
        "query": q,
        "limit": limit,
        "offset": offset,
        "results": dummy_data[offset:offset + limit],
        "message": "검색 성공"
    }


# q: Annotated[
#     str, 
#     Query(
#         min_length=3, 
#         max_length=50, 
#         pattern="^[a-zA-Z0-9가-힣\s]+$",  # 한글/영어/숫자/공백만 허용
#         description="검색 키워드 (특수문자 불가)"
#     )
# ] = ...

# limit: Annotated[
#     int,
#     Query(
#         ge=1,       # 최소 1
#         le=100,     # 최대 100
#         description="최대 결과 수"
#     )
# ] = 5

# q: 빨간사과
# limit: 5
# offset: 0

# http://127.0.0.1:8000/search?q=사과&limit=5&offset=0
# http://127.0.0.1:8000/search?q=검색어&limit=개수&offset=시작지점
# http://127.0.0.1:8000/search?q=apple&limit=5&offset=0


# Method: GET
# URL: http://127.0.0.1:8000/search
# Params (쿼리):
# q: 녹색사과
# limit: 5
# offset: 0