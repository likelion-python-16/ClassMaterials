# 먼저 beautifulsoup4가 설치되어 있어야 합니다
# pip install beautifulsoup4

# 필요한 라이브러리 가져오기
import requests  # 웹 페이지 요청을 보내기 위한 라이브러리
from bs4 import BeautifulSoup  # HTML을 파싱(분석)하기 위한 라이브러리
import json  # JSON 파일로 저장하기 위한 기본 내장 모듈

# 1. 웹 페이지 주소 지정
url = "https://quotes.toscrape.com/"

# 2. 해당 웹 페이지에 요청을 보내고, 응답(response)을 받아온다
response = requests.get(url)

# 3. 응답받은 HTML 내용을 BeautifulSoup으로 파싱해서 soup 객체로 만든다
soup = BeautifulSoup(response.text, "html.parser")

# 4. 명언 데이터를 담을 빈 리스트 만들기
quotes = []

# 5. 웹 페이지 내에서 class가 "quote"인 요소들을 모두 찾아 반복한다
for quote in soup.select(".quote"):
    # 명언 텍스트를 선택하고, 문자열만 깔끔하게 추출
    text = quote.select_one(".text").get_text(strip=True)
    
    # 작가 이름도 선택해서 문자열만 추출
    author = quote.select_one(".author").get_text(strip=True)

    # 추출한 데이터를 딕셔너리 형태로 저장하고, 리스트에 추가
    quotes.append({
        "quote": text,
        "author": author
    })

# 6. 리스트 안의 딕셔너리들을 평탄화 (2단계 구조를 1단계로 바꾸기)
# 예: {"quote": "...", "author": "..."} → {"0 : quote": "...", "0 : author": "..."}
flat_data = {}
for i, item in enumerate(quotes):  # quotes 리스트를 인덱스와 함께 반복
    for key, value in item.items(): # 각 딕셔너리의 key, value를 꺼냄
        flat_data[f"{i} : {key}"] = value  # 키 이름을 인덱스와 함께 구성

# 7. 평탄화된 데이터를 JSON 파일로 저장
with open("data/crawl_and_flatten.json", "w", encoding="utf-8") as f:
    # JSON 형태로 저장하고, 한글이 깨지지 않게 설정 (ensure_ascii=False)
    # 보기 좋게 들여쓰기(indent=2) 설정
    json.dump(flat_data, f, ensure_ascii=False, indent=2)

# 8. 완료 메시지 출력
print("✔ flattened.json 생성됨")
