import requests
from typing import List, Dict

class MusinsaAPI():
    def __init__(self, keyword:str = "할인", page: int = 1, size: int = 60):
        # API 엔드포인트
        self.url = "https://api.musinsa.com/api2/dp/v1/plp/goods"
        # 요청 파라미터 설정
        self.params ={
            "gf": "A",
            "keyword": keyword,
            "sortCode": "POPULAR",
            "page": page,
            "size": size,
            "caller": "SEARCH",
        }
        self.headers = {
            "User-Agent":(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/138.0.0.0 Safari/537.36"
        ),
        "Accept":"application/json, text/plain, */*",
        }
    # [{"keyword": keyword, "page": page}] # Get요청 수행
    def fetch(self) -> List[Dict]:  
        response = requests.get(self.url, params=self.params, headers=self.headers) 
        response.raise_for_status()
        data = response.json()

        # 딕셔너리에서 안전하게 값을 꺼내오는 값을 조회하고 조건 검사하는 구문이다.
        goods_list = data.get("data", {}).get("list", [])
        if not goods_list:
            return []

        result: List[Dict] = []
        for g in goods_list:
            result.append({
                "goodsNo": g.get("goodsNo"),
                "name": g.get("goodsName", ""),
                "brand": g.get("brandName", ""),
                "normalPrice": f"{g.get("normalPrice", 0)}원",
                "saleprice": f"{g.get("price", 0)}원",
                "linkUrl": "https://api.musinsa.com/" + g.get("goodsLinkUrl", ""),
                "imageUrl": g.get("thumbnail", ""), 
            })  
        return result   

# 출력구문
if __name__ == "__main__":
    api = MusinsaAPI(keyword="신발", size=5)
    items = api.fetch()
    print(items)
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {item['name']} - {item['saleprice']} {item['imageUrl']} ({item['linkUrl']})")
    
    
    
    