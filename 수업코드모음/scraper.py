import requests

class MusinsaAPI:
    def __init__(self):
        self.url = "https://api.musinsa.com/api2/dp/v1/plp/goods"
        self.params = {
            "gf":"A",
            "keyword":"할인",
            "sortCode":"POPULAR",
            "page":1,
            "size":60,
            "caller":"SEARCH",
        }
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/138.0.0.0 Safari/537.36",
            "Accept":"application/json, text/plain, */*",
        }

    def fetch(self):
        resp = requests.get(self.url, params=self.params, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()
        goods_list = data["data"]["list"]

        result = []
        for g in goods_list:
            result.append({
                "goodsNo":g.get("goodsNo"),
                "name":g.get("goodsName"),
                "brand":g.get("brand", ""),
                "originalPrice":f"{g.get('normalPrice',0)}원",
                "salePrice":f"{g.get('price',0)}원",
                "url":"https://www.musinsa.com" + g.get("goodsLinkUrl",""),
                "image":g.get("thumbnail",""),
            })
        return result

if __name__ == "__main__":
    api = MusinsaAPI()
    items = api.fetch()
    for item in items[:5]:
        print(item)