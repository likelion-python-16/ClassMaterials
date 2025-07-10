```bash
# 기본 요청 라이브러리 (동기 방식)
pip install requests

# 비동기 방식 (성능이 중요할 경우)
pip install aiohttp aiodns
```

공공데이터를 사용하려면:
1. API 주소(URL) 를 확인하고
2. 인증키(서비스 키) 를 넣어서
3. 원하는 데이터를 요청하고
4. 받은 JSON 데이터를 파이썬으로 처리합니다

aiohttp는 비동기 HTTP 클라이언트/서버 프레임워크입니다. 주로 `asyncio` 기반의 비동기 웹 요청이나 비동기 웹 서버를 만들 때 사용합니다.

비동기 방식으로 HTTP 요청을 보내고 JSON 데이터를 받아오는 테스트코드:
Jupyter에서 테스트하기:
```python
import aiohttp
import json

async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
    async with session.get("https://dummyjson.com/products") as resp:
        j = await resp.json()
        print(json.dumps(j, indent=2))
```
- 실제 공공데이터 API나 REST API를 사용할 때도 이런 방식으로 데이터를 받아오게 됩니다.
- `aiohttp`는 빠른 처리를 원할 때 사용하는 비동기 방식이라 연습해보는 겁니다.
- `https://dummyjson.com`은 테스트용 API로, 실습할 때 서버에 피해 없이 자유롭게 테스트할 수 있어요.

---
공공체이터 포털에서 지난 날씨 데이터 가지고 오기
![[Pasted image 20250710185106.png]]

공공데이터포털
https://www.data.go.kr/data/15059093/openapi.do

검색어로 종관이라고 검색
![[Pasted image 20250710185416.png]]

![[Pasted image 20250710185526.png]]

활용신청:
![[Pasted image 20250710185707.png]]

활용신청:
![[Pasted image 20250710190040.png]]

모듈 호출 및 함수작성:
```python
import requests

def get_weather_data():
```


API url 요청주소에 있는 것을 작성한다.
```python
url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
```
![[Pasted image 20250710191109.png]]

일반 인증키를 잘 보관해 두세요:
![[Pasted image 20250710193701.png]]

요청변수: 인코딩된 서비스키를 사용해야함
```python
    params = {
        "serviceKey": "SRxa9dZt5WirGiT%2Fhc8U%2B%2BALRzFkzGR51qSlYbmID9oXRmUH8PfCxRC%2BvAtqqlrPVSLSaiM0TiWCj6q40N0ilQ%3D%3D",
        "dataType": "JSON",
        "numOfRows": 10,
        "pageNo": 1,
        "dataCd": "ASOS",
        "dateCd": "DAY",
        "startDt": "20250101",
        "endDt": "20250106",
        "stnIds": "108"
    }
```
![[Pasted image 20250710190502.png]]

---

API 서버에 **GET 요청**을 보내는 함수
```python
response = requests.get(url, params=params)
data = response.json()
```

이 코드는 모든 데이터를 돌려본 샘플 데이터 입니다
```python
    """
    {
        "response":{
            "header":{
                "resultCode":"00",
                "resultMsg":"NORMAL_SERVICE"
            },
            "body":{
                "dataType":"JSON",
                "items":{
                    "item":[
                    {
                        "stnId":"108",
                        "stnNm":"서울",
                        "tm":"2022-01-01",
                        "avgTa":"-4.3",
                        "minTa":"-10.2",
                        "minTaHrmt":"0710",
                        "maxTa":"2.3",
                        "maxTaHrmt":"1544",
                        "mi10MaxRn":"",
                        "mi10MaxRnHrmt":"",
                        "hr1MaxRn":"",
                        "hr1MaxRnHrmt":"",
                        "sumRnDur":"",
                        "sumRn":"",
                        "maxInsWs":"4.5",
                        "maxInsWsWd":"70",
                        "maxInsWsHrmt":"0923",
                        "maxWs":"2.8",
                        "maxWsWd":"20",
                        "maxWsHrmt":"0819",
                        "avgWs":"1.5",
                        "hr24SumRws":"1335",
                        "maxWd":"50",
                        "avgTd":"-14.4",
                        "minRhm":"31",
                        "minRhmHrmt":"1329",
                        "avgRhm":"46.3",
                        "avgPv":"2.1",
                        "avgPa":"1019.8",
                        "maxPs":"1034.0",
                        "maxPsHrmt":"0247",
                        "minPs":"1027.3",
                        "minPsHrmt":"2351",
                        "avgPs":"1030.9",
                        "ssDur":"9.6",
                        "sumSsHr":"9.0",
                        "hr1MaxIcsrHrmt":"1200",
                        "hr1MaxIcsr":"1.82",
                        "sumGsr":"10.39",
                        "ddMefs":"",
                        "ddMefsHrmt":"",
                        "ddMes":"",
                        "ddMesHrmt":"",
                        "sumDpthFhsc":"",
                        "avgTca":"1.4",
                        "avgLmac":"1.4",
                        "avgTs":"-3.7",
                        "minTg":"-15.4",
                        "avgCm5Te":"-0.9",
                        "avgCm10Te":"-1.0",
                        "avgCm20Te":"-0.3",
                        "avgCm30Te":"0.9",
                        "avgM05Te":"2.7",
                        "avgM10Te":"6.6",
                        "avgM15Te":"10.1",
                        "avgM30Te":"15.1",
                        "avgM50Te":"17.2",
                        "sumLrgEv":"1.3",
                        "sumSmlEv":"1.8",
                        "n99Rn":"0.3",
                        "iscs":"",
                        "sumFogDur":""
                    }
                    ]
                },
                "pageNo":1,
                "numOfRows":2,
                "totalCount":1
            }
        }
    }
    """
```

필요한 데이터만 수집:
```python
    if data["response"]["header"]["resultCode"] == "00":
        item_list = data["response"]["body"]["items"]["item"]
        dict_list = []
        for item in item_list:
            item_dict = {}
            item_dict["date"] = item["tm"] # 시간
            item_dict["min_temp"] = item["minTa"] # 최저 기온
            item_dict["max_temp"] = item["maxTa"] # 최고 기온
            item_dict["cloud_amount"] = item["avgTca"] # 평균 전운량
            item_dict["max_snow"] = item["ddMes"] # 일 최심적설
            item_dict["rain"] = item["sumRn"] # 일강수량
            dict_list.append(item_dict)
        return dict_list
    else:
        return None
```

 Jupyter에서 실행:
```python
from api_scrap.weather_data import get_weather_data
get_weather_data()
```