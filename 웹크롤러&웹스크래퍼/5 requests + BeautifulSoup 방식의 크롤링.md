[https://www.crummy.com/software/BeautifulSoup/bs4/doc.ko/](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ko/)

사이트주소 http://www.cgv.co.kr/movies/?lt=1&ft=0

BeautifulSoup & HTML 파서
```
pip install beautifulsoup4
pip install beautifulsoup4 lxml

pip list # 설치확인
```
BeautifulSoup은 HTML 파서를 직접 제공하지 않기 때문에 `lxml` 또는 `html5lib` 중 하나도 함께 설치하는 것이 좋습니다

```python
# requests와 BeautifulSoup 라이브러리를 불러온다. (웹페이지 요청 및 HTML 파싱용)
import requests
from bs4 import BeautifulSoup

# CGV 영화 정보를 수집하는 함수 정의
def get_cgv_movies():
    # CGV 영화 페이지 URL을 변수에 저장
    url = "http://www.cgv.co.kr/movies/"

    # 요청할 때 사용하는 헤더(User-Agent)는 브라우저처럼 보이게 하기 위해 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }

    # 웹페이지에 GET 요청을 보내고 응답을 받아온다
    resp = requests.get(url, headers=headers)

    # 요청이 실패하면 예외를 발생시켜 프로그램을 중단시킨다
    resp.raise_for_status()

    # 받은 HTML 문서를 BeautifulSoup을 이용해 파싱한다 
    # (html.parser는 파서 종류)
    soup = BeautifulSoup(resp.text, "html.parser")

    # 영화 목록이 들어 있는 태그(ol > li)를 모두 선택하여 리스트로 저장
    chart_box = soup.select("div.sect-movie-chart ol li")
```

왜 이런 순서로 해야 할까?
- 먼저 웹페이지에 접속해야 응답이 생기고
- 응답이 정상인지 확인하고
- 그 응답 안의 HTML을 파싱하고
- 그 HTML 안에서 필요한 정보를 선택합니다.

비유로 정리하면:
택배 상자 받기 → 상자에 문제가 없는지 확인 → 상자 열기 → 안에서 정보 찾기


```python
# 결과를 담을 리스트를 미리 만들어 놓는다
    result = []

    # 영화 하나하나씩 반복하면서 정보를 추출한다
    for movie in chart_box:
    
        # 영화 제목이 들어 있는 <strong class="title"> 태그를 찾는다
        title_tag = movie.select_one("strong.title")
        
        # 예매율이 들어 있는 <strong class="percent"> 태그 내부의 <span>을 찾는다
        percent_tag = movie.select_one("strong.percent span")
        
        # 개봉일 정보가 들어 있는 <span class="txt-info"> 태그를 찾는다
        release_tag = movie.select_one("span.txt-info")
        
        # 영화 포스터 이미지를 나타내는 <img> 태그를 찾는다
        img_tag = movie.select_one("img")
```

태그 분석의 주요 기준:
태그 이름:	`<div>, <span>, <a>` 등 ( 예시:`soup.find('div')`)

클래스명(class):	대부분의 사이트가 디자인/구조 분리를 위해 많이 사용	
( 예시: `soup.select('.title')`)

id 속성:	페이지에서 유일함 (단 하나의 요소 찾기에 적합)	
( 예시:`soup.select('#main')`)

태그의 위치(계층 구조):	부모-자식 구조를 통해 위치 기반으로 탐색	
( 예시:`div.container > ul > li`)

속성(attribute): `href, src, data-*, title` 등	
( 예시:`soup.find('a', href=True)`)

텍스트 내용:	텍스트 자체를 기준으로 필터링	( 예시:`if "CGV" in tag.text:`)

메서드 정리:
`find():` 태그 기반 (한 개)
`find_all()`: 태그 기반 (여러 개)
`select()`: CSS 선택자 방식 (여러 개)
`select_one()`: CSS 선택자 방식 (한 개)

`find()` 사용 시 (속성 기반)
```python
soup.find("div", class_="title")      # class명
soup.find("div", id="main")           # id명
```

`select()` 사용 시 (CSS 선택자 방식)
```python
soup.select("div.title")              # class명
soup.select("div#main")               # id명
soup.select("div.box > ul > li")      # 위치 기반 선택
```

```python
percent_tag = movie.select_one("strong.percent span")
```
해석: 이 구조에서 `span`을 가져오려는 겁니다.
```html
<strong class="percent">
    <span>예매율 52%</span>
</strong>
```
---
조건부 파싱 + 딕셔너리 구성을 동시에 처리
```python
        # 제목이 있는 경우에만 정보를 result 리스트에 추가한다
        if title_tag:
            result.append({
                "title": title_tag.text.strip(),  
                # 제목 텍스트에서 양쪽 공백 제거 후 저장
                
                "reserve_percent": percent_tag.text.strip() if percent_tag else None,  
                # 예매율이 있다면 텍스트 저장, 없으면 None
                
                "release_date": release_tag.text.strip() if release_tag else None,  
                # 개봉일이 있다면 텍스트 저장, 없으면 None
                
                "poster": img_tag["src"] if img_tag else None  
                # 포스터 이미지의 src 속성값을 저장
            })
    
    # 최종적으로 영화 정보를 담은 리스트를 반환한다
    return result
```

- `title_tag`에서 텍스트만 뽑고 양쪽 공백 제거 (`strip()`)
- 예: `<strong class="title"> 쥬라기 월드 </strong>` → `"쥬라기 월드"`

- 개봉일 정보를 가진 `release_tag`가 있으면 텍스트 추출 없으면 `None` (정보가 누락된 경우 대비)

- 포스터 이미지를 담고 있는 `<img>` 태그가 있다면 → `src` 속성값만 가져옴 (이미지 주소) 없으면 `None`  
- 예: `<img src="https://...jpg">` → `"https://...jpg"`

---
```python
# 이 파일이 메인으로 실행될 때만 아래 코드가 실행되도록 설정
if __name__ == "__main__":
    # 위에서 정의한 함수 실행 → 영화 정보 리스트 가져오기
    movies = get_cgv_movies()

    # 영화 리스트를 반복문으로 출력 (번호와 함께 출력)
    for i, m in enumerate(movies, 1): # 인덱스 1부터  
    # enumerate는 번호(1부터)와 데이터를 함께 반환
    
        print(f"{i}. {m['title']} ({m['release_date']}) - 예매율: {m['reserve_percent']}")
```

예상 출력결과:
```
1. 쥬라기 월드 (2025.07.04) - 예매율: 52.3%
```