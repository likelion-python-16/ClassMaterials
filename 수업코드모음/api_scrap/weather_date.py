import requests


def get_weather_data():
    url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
    params = {
        # 인코딩
        # "serviceKey": "SRxa9dZt5WirGiT%2Fhc8U%2B%2BALRzFkzGR51qSlYbmID9oXRmUH8PfCxRC%2BvAtqqlrPVSLSaiM0TiWCj6q40N0ilQ%3D%3D",
        # 디코딩
        "serviceKey":"SRxa9dZt5WirGiT/hc8U++ALRzFkzGR51qSlYbmID9oXRmUH8PfCxRC+vAtqqlrPVSLSaiM0TiWCj6q40N0ilQ==",
        "dataType": "JSON",
        "numOfRows": 10,
        "pageNo": 1,
        "dataCd": "ASOS",
        "dateCd": "DAY",
        "startDt": "20250101",
        "endDt": "20250106",
        "stnIds": "108"
  }
    response = requests.get(url, params=params)
    data = response.json()
    
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