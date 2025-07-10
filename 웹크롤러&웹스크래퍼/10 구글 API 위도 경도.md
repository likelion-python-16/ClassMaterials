Google Maps API를 활용한 위치 데이터 추출
목표: 
	Google Maps Geocoding API를 사용하여 주소로부터 음식점의 위도와 경도 데이터 추출하기.
학습내용:
	Google API 키 생성, Geocoding API 사용법, Python을 이용한 데이터 추출.

구글에서 새프로젝트 만들기
[https://console.cloud.google.com/welcome?inv=1&invt=Ab2YCA&project=stately-furnace-424809-k0](https://console.cloud.google.com/welcome?inv=1&invt=Ab2YCA&project=stately-furnace-424809-k0)
![[Pasted image 20250710202334.png]]
![[Pasted image 20250710202419.png]]


Google Cloud Console:[https://developers.google.com/maps/documentation/geocoding/overview?hl=ko](https://developers.google.com/maps/documentation/geocoding/overview?hl=ko)

Geocoding 시작하기
![[Pasted image 20250710201620.png]]

그외 정보를 입력하고 카드결제도 연동하면 최종적으로 API키가 생성됩니다
![[Pasted image 20250710202754.png]]
이 키는 잘 보관해 둬야 합니다

![[Pasted image 20250710203044.png]]
![[Pasted image 20250710203125.png]]![[Pasted image 20250710203234.png]]

![[Pasted image 20250710203301.png]]

googlemaps 
```bash
pip install googlemaps
```

geocoding.py
```python
import googlemaps

def geocode_address(address):
    gmaps = googlemaps.Client(key='구글API key를 넣는다')
    geocode_result = gmaps.geocode(address)
    return geocode_result
```

jupyter
```python
from api_scrap.geocoding import geocode_address
geocode_address("서울역")
```

결과:
```json
[{'address_components': [{'long_name': 'Seoul Station (Subway)',
    'short_name': 'Seoul Station (Subway)',
    'types': ['establishment',
     'point_of_interest',
     'subway_station',
     'transit_station']},
   {'long_name': '2', 'short_name': '2', 'types': ['premise']},
   {'long_name': 'Sejong-daero 18-gil',
    'short_name': 'Sejong-daero 18-gil',
    'types': ['political', 'sublocality', 'sublocality_level_4']},
   {'long_name': '소공동',
    'short_name': '소공동',
    'types': ['political', 'sublocality', 'sublocality_level_2']},
   {'long_name': 'Jung District',
    'short_name': 'Jung District',
    'types': ['political', 'sublocality', 'sublocality_level_1']},
   {'long_name': 'Seoul',
    'short_name': 'Seoul',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': 'South Korea',
    'short_name': 'KR',
    'types': ['country', 'political']},
   {'long_name': '100-102',
    'short_name': '100-102',
    'types': ['postal_code']}],
  'formatted_address': 'Seoul Station (Subway), 2 Sejong-daero 18-gil, 소공동 Jung District, Seoul, South Korea',
  'geometry': {'location': {'lat': 37.555946, 'lng': 126.972317},
   'location_type': 'ROOFTOP',
   'viewport': {'northeast': {'lat': 37.55729498029149,
     'lng': 126.9736659802915},
    'southwest': {'lat': 37.5545970197085, 'lng': 126.9709680197085}}},
  'partial_match': True,
  'place_id': 'ChIJA3CU42aifDURaq-3csGXvuc',
  'plus_code': {'compound_code': 'HX4C+9W Seoul, South Korea',
   'global_code': '8Q98HX4C+9W'},
  'types': ['establishment',
   'point_of_interest',
   'subway_station',
   'transit_station']},
 {'address_components': [{'long_name': 'Seoul',
    'short_name': 'Seoul',
    'types': ['establishment',
     'point_of_interest',
     'subway_station',
     'transit_station']},
   {'long_name': 'Seoul',
    'short_name': 'Seoul',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': 'South Korea',
    'short_name': 'KR',
    'types': ['country', 'political']}],
  'formatted_address': 'Seoul, Seoul, South Korea',
  'geometry': {'location': {'lat': 37.553514, 'lng': 126.972713},
   'location_type': 'GEOMETRIC_CENTER',
   'viewport': {'northeast': {'lat': 37.5548629802915,
     'lng': 126.9740619802915},
    'southwest': {'lat': 37.5521650197085, 'lng': 126.9713640197085}}},
  'partial_match': True,
  'place_id': 'ChIJl_j43maifDURxrUjyba9V64',
  'plus_code': {'compound_code': 'HX3F+C3 Seoul, South Korea',
   'global_code': '8Q98HX3F+C3'},
  'types': ['establishment',
   'point_of_interest',
   'subway_station',
   'transit_station']}]
```

![[Pasted image 20250710211107.png]]

jupyter
```python
from api_scrap.geocoding import geocode_address
geocode_address("서울 강남구 선릉로158길")
```

결과:
```
[{'address_components': [{'long_name': 'Seolleung-ro 158-gil',
    'short_name': 'Seolleung-ro 158-gil',
    'types': ['political', 'sublocality', 'sublocality_level_4']},
   {'long_name': 'Gangnam District',
    'short_name': 'Gangnam District',
    'types': ['political', 'sublocality', 'sublocality_level_1']},
   {'long_name': 'Seoul',
    'short_name': 'Seoul',
    'types': ['administrative_area_level_1', 'political']},
   {'long_name': 'South Korea',
    'short_name': 'KR',
    'types': ['country', 'political']},
   {'long_name': '06014', 'short_name': '06014', 'types': ['postal_code']}],
  'formatted_address': 'Seolleung-ro 158-gil, Gangnam District, Seoul, South Korea',
  'geometry': {'bounds': {'northeast': {'lat': 37.5265706, 'lng': 127.0416803},
    'southwest': {'lat': 37.5249694, 'lng': 127.0403286}},
   'location': {'lat': 37.5257424, 'lng': 127.0411066},
   'location_type': 'APPROXIMATE',
   'viewport': {'northeast': {'lat': 37.5271189802915,
     'lng': 127.0423534302915},
    'southwest': {'lat': 37.5244210197085, 'lng': 127.0396554697085}}},
  'place_id': 'ChIJbQfFEHikfDUREby0ysH4HS0',
  'types': ['political', 'sublocality', 'sublocality_level_4']}]
```

원하는 데이터만 추출하기:
```python
import googlemaps
from anyio import sleep

def geocode_address(address):
    gmaps = googlemaps.Client(key='AIzaSyCs6iNDVPjAcoGLDpKhivAJ6R9VRqCfIUs')
    geocode_result = gmaps.geocode(address)
    # return geocode_result

# 필요한 정보만 가져오기
    sleep(1)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        return None
```

jupyter
```python
from api_scrap.geocoding import geocode_address
geocode_address("서울 강남구 선릉로158길")
```

결과:
```bash
(37.5257424, 127.0411066)
```