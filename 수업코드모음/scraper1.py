import requests

class MusinsaBannerAPI:
    def __init__(self):
        self.url = "https://api.musinsa.com/api2/hm/web/v4/pans/recommend"
        self.params = {
            "storeCode": "musinsa",
            "gf": "A",
            "page": 2,
            "size": 10,
            "index": 16,
            "scenarioIndex": 8,
        }

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
        }

    def fetch(self):
        resp = requests.get(self.url, params=self.params, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()

        # ✅ 추가
        print("[DEBUG] data keys:", data.keys())
        print("[DEBUG] full response preview:", data)

        modules = data.get("data", {}).get("modules", [])
        result = []
        for module in modules:
            if module.get("type") == "BANNER_MAIN":
                for item in module.get("items", []):
                    result.append({
                        "id": item.get("id"),
                        "title": item.get("info", {}).get("title", {}).get("text", ""),
                        "subTitle": item.get("info", {}).get("subTitle", {}).get("text", ""),
                        "image": item.get("image", {}).get("url", ""),
                        "url": item.get("url", ""),
                    })
        return result

if __name__ == "__main__":
    api = MusinsaBannerAPI()
    banners = api.fetch()  # ✅ 수정된 부분
    for banner in banners:
        print(banner)
