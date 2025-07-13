https://blog.naver.com/gangbuk_official/223177144192

이 블러그 같은 경우는 네이버 블로그 데스크탑 버전은 본문이 iframe 안에 있어서 requests로는 직접 접근이 안 되고, JavaScript 실행이 필요한 구조라서 경우에 따라 웹드라이버(Selenium) 가 필요한 상태의 크로링 방식입니다.

- 네이버 블로그 리뷰를 수집한다.
- iframe 구조 대응을 고려한다.
- SEO(검색 결과)에 노출된 블로그 중, 특정 키워드가 포함된 글만 필터링한다.
- 본문에서 불필요한 텍스트 제거(예: 블로그기자단) 등 후처리(cleaning) 작업도 포함한다.

`requests`
용도: 정적인 HTML, JSON, XML 등 데이터를 서버에서 직접 요청해서 가져올 때 사용

JSON API 호출:
```python
import requests
response = requests.get("https://api.example.com/data")
data = response.json()
```
정적인 HTML 가져오기:
```pythoh
html = requests.get("https://example.com").text
```
`requests`는 자바스크립트가 렌더링한 DOM 결과는 가져오지 못함

---
`BeautifulSoup`:
용도: HTML/XML 파싱용 도구  
HTML 문서 안에서 원하는 태그나 내용을 추출할 때 사용

HTML에서 `<div class="title">`만 추출:
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
title = soup.find("div", class_="title").text
```
`BeautifulSoup`은 HTML을 파싱만 할 뿐, 크롤링(요청)은 못함 → 보통 `requests`와 함께 사용

---
`selenium`
용도: 자바스크립트 기반의 동적 페이지를 제어/크롤링할 때 사용  
브라우저를 실제 사용자가 조작하듯 실행시켜서 렌더링 결과를 받아옴

- 네이버 블로그 본문처럼 iframe 내부 JS 렌더링된 데이터 추출
- 로그인, 클릭, 무한스크롤, 페이지 이동 등 사용자 인터랙션 구현 가능
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")
driver.find_element(By.ID, "loadButton").click()
html = driver.page_source
```
- 상대적으로 느림, 리소스 소모 큼
- 간단한 정적 페이지엔 불필요

크롤링 선택시 적용기준
- API가 있다 → `requests + json()`
- 정적 HTML 페이지 → `requests + BeautifulSoup`
- 동적 JS 렌더링 페이지 → `Selenium (+ BeautifulSoup)`


```python
import re
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
```


텍스트를 정제 (공백/보이지 않는 문자 제거) → 상기 두 `crawl_` 함수에서 사용됨
```python
# 문자 및 줄바꿈 제거 함수
def clean_text(text):
    # 모든 제어 문자 제거 (유니코드 category C*)
    text = "".join(c for c in text if not unicodedata.category(c).startswith("C"))
    # 중복 공백 제거
    text = re.sub(r"[ \t\n\r\f\v]+", " ", text)
    return text.strip()
```

위 함수가 없으면 아래와같이 특수문자가 같이 크롤링이 됩니다.
![[Pasted image 20250709082520.png]]

이 함수가 사용된 위치:
```python
content = content.text
cleaned_content = clean_text(content)  # 여기!
return cleaned_content
```

---
하는 일: 
- Selenium을 이용해 실제 네이버 블로그의 본문을 불러옴 (자바스크립트 렌더링 필요).
- 블로그 본문은 iframe에 들어 있어서, iframe 내부로 진입해야 `본문 영역`에 접근 가능.
```python
# Selenium 기반 iframe 내부 본문 추출 함수(JS 렌더링 필요)
def crawl_naver_blog(url):
    # Set up webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,)
    # 블로그 URL 열기
    driver.get(url)

    # iframe 내부로 이동
    iframe_element = driver.find_element(By.ID, "mainFrame")  # iframe의 id를 사용하여 찾는 예시
    driver.switch_to.frame(iframe_element)  # iframe 내부로 전환

    # iframe 안의 콘텐츠 로딩 대기 후 HTML 추출
    driver.find_element(By.ID, "post-area")  # iframe 안의 엘리먼트의 class로 찾는 예시
    res = driver.page_source
    driver.quit()

    # BeautifulSoup로 HTML 파싱 및 본문 텍스트 추출
    soup = BeautifulSoup(res, "html.parser")
    content = soup.find("div", {"class": "se-main-container"})
    if content is None:
        content = soup.find("div", {"id": "post-area"})
    span_tag = content.find("span", text=re.compile("블로그기자단"))
    if span_tag:
        span_tag.decompose()
    content = content.text
    content = re.sub(r"\n+", " ", content)
    return content
```

- Chrome WebDriver 실행 (headless 모드)
- 블로그 주소 접근 → iframe(`id="mainFrame"`)으로 진입
- 본문 HTML 추출 후 BeautifulSoup으로 파싱
- 본문에서 `"se-main-container"` 또는 `"post-area"` 찾기
- `"블로그기자단"` 문구가 포함된 `span` 제거
- `.text`로 텍스트 추출
- `clean_text()`로 텍스트 정제
- 정제된 결과 `return`

---
하는 일: 
- 자바스크립트 렌더링이 필요 없는 경우, iframe 구조만 따라가서 본문을 크롤링.
- Selenium보다 속도가 빠름.
- iframe에서 실제 본문 HTML을 `requests.get()`으로 따로 가져옴.
```python
# requests 기반 크롤링 (iframe 내부도 HTML 요청)
def crawl_naver_blog_by_requests(url):
    res = requests.get(url)
    root_url = "https://blog.naver.com"

     # iframe이 있을 경우 별도 요청
    if 'id="mainFrame"' in res.text:
        soup = BeautifulSoup(res.text, "html.parser")
        iframe = soup.find("iframe", {"id": "mainFrame"})
        iframe_src = iframe["src"]
        res = requests.get(root_url + iframe_src)

    # 본문 파싱 및 추출
    soup = BeautifulSoup(res.text, "html.parser")
    content = soup.find("div", {"class": "se-main-container"})
    if content is None:
        content = soup.find("div", {"id": "post-area"})
    # 불필요한 태그 제거 및 텍스트 정제
    span_tag = content.find("span", text=re.compile("블로그기자단"))
    if span_tag:
        span_tag.decompose()
    content = content.text
    content = re.sub(r"\n+", " ", content)
    return content
```
`requests` 기반으로 iframe 내부 글을 크롤링

- 초기 요청: 블로그 HTML 로드
- iframe 존재 시 → `iframe src` 추출하여 재요청
- 본문 container 추출: `"se-main-container"` 또는 `"post-area"`
- `"블로그기자단"` 태그 제거
- `.text`로 텍스트 추출
- `clean_text()`로 텍스트 정제
- 정제된 텍스트 `return`

---
하는 일: 
- 네이버 검색결과 페이지에서 `블로그 리뷰 링크` 추출
- `<a class="title_link">` 들 중에서 `title`에 특정 키워드가 포함된 항목만 필터링
```python
# 네이버 검색 결과에서 블로그 리뷰 링크를 수집하는 함수
def find_reivew_article(location: str, keyword: str):
    url = f"https://search.naver.com/search.naver?sm=tab_hty.top&ssc=tab.blog.all&query={location}+{keyword}+리뷰"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 검색 결과 중 블로그 글 링크 찾기
    title_link = soup.find_all("a", class_="title_link")
    review_list = []
    for t_l in title_link:
        title = t_l.text
        href = t_l["href"]
        if keyword in title:
            review_list.append((title, href))

    return review_list
```

- 네이버 검색 URL 구성
- 결과 HTML 파싱
- `<a class="title_link">` 목록 추출
- 제목에 keyword가 포함된 링크만 수집
- 리스트로 반환 → `[("제목", "링크"), ...]`

---
jupyter 실행
```python
import sys, os
sys.path.append(os.getcwd())

from selenium_crawler.naver_blog_scrap2 import crawl_naver_blog_by_requests
crawl_naver_blog_by_requests("https://blog.naver.com/gangbuk_official/223177144192")
```