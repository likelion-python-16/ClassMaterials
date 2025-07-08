import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# 문자 및 줄바꿈 제거 함수
def clean_text(text):
    # 모든 제어 문자 제거 (유니코드 category C*)
    text = "".join(c for c in text if not unicodedata.category(c).startswith("C"))
    # 중복 공백 제거
    text = re.sub(r"[ \t\n\r\f\v]+", " ", text)
    return text.strip()

# Selenium 기반 iframe 내부 본문 추출 함수(JS 렌더링 필요)
def crawl_naver_blog(url):
    # 1. WebDriver 옵션 설정 (헤드리스 모드)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,)
    
    # 2. 데스크탑 네이버 블로그 URL 열기
    driver.get(url)

   # 3. mainFrame iframe 내부로 전환하여 실제 포스트 내용 로드
    iframe_element = driver.find_element(By.ID, "mainFrame")  # iframe의 id를 사용하여 찾는 예시
    driver.switch_to.frame(iframe_element)  # iframe 내부로 전환

    # 4. post-area 요소가 로드될 때까지 대기 (본문 영역 확인)
    driver.find_element(By.ID, "post-area")  # iframe 안의 엘리먼트의 class로 찾는 예시
    res = driver.page_source
    driver.quit()

    # 5. BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(res, "html.parser")

    # 6. 새 에디터(se-main-container) 또는 기존(post-area)에서 본문 컨테이너 찾기
    content = soup.find("div", {"class": "se-main-container"}) # 본문컨테이너  m.에서 찾은것
    if content is None:
        content = soup.find("div", {"id": "post-area"}) #  아이프레임

    # 7. 스팸 태그(블로그기자단) 제거    
    span_tag = content.find("span", text=re.compile("블로그기자단"))
    if span_tag:
        span_tag.decompose()

     # 8. 텍스트만 추출하고 줄바꿈 제거
    content = content.text
    cleaned_content = clean_text(content)
    return cleaned_content

# requests 기반 크롤링 (iframe 탐지 후 추가 요청)
def crawl_naver_blog_by_requests(url):

    # 1. 초기 요청
    res = requests.get(url)
    root_url = "https://blog.naver.com"

    # 2. iframe 감지: desktop 페이지는 iframe으로 포스트 로드
    if 'id="mainFrame"' in res.text:
        soup = BeautifulSoup(res.text, "html.parser")
        iframe = soup.find("iframe", {"id": "mainFrame"})
        iframe_src = iframe["src"]
        
        # 3. iframe src에 재요청하여 실제 HTML 가져오기
        res = requests.get(root_url + iframe_src)

    # 4. BeautifulSoup 파싱
    soup = BeautifulSoup(res.text, "html.parser")

    # 5. 본문 컨테이너 찾기 (새/기존 에디터)
    content = soup.find("div", {"class": "se-main-container"})
    if content is None:
        content = soup.find("div", {"id": "post-area"})
    
    # 6. 스팸 태그 제거 및 텍스트 정제
    span_tag = content.find("span", text=re.compile("블로그기자단"))
    if span_tag:
        span_tag.decompose()
    content = content.text
    cleaned_content = clean_text(content)
    return cleaned_content

# 네이버 검색 결과에서 블로그 리뷰 링크를 수집하는 함수
# - location과 keyword로 리뷰 포스트 검색
# - 검색 결과에서 제목에 keyword가 포함된 링크만 추출

# 하는 일: 네이버 검색 결과 페이지에서 리뷰 키워드가 포함된 블로그 링크 수집
# 기술: requests.get() → BeautifulSoup으로 <a class="title_link">들 추출
def find_reivew_article(location: str, keyword: str):
    
    # 1. 네이버 검색 URL 생성 (블로그 탭, 리뷰 키워드)
    url = f"https://search.naver.com/search.naver?sm=tab_hty.top&ssc=tab.blog.all&query={location}+{keyword}+리뷰"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 2. 결과 목록에서 블로그 글 링크 요소 추출
    title_link = soup.find_all("a", class_="title_link")
    review_list = []
    
    for t_l in title_link:
        title = t_l.text
        href = t_l["href"]
        if keyword in title:
            review_list.append((title, href))


    return review_list


# import sys, os
# sys.path.append(os.getcwd())

# from selenium_crawler.naver_blog_scrap2 import crawl_naver_blog_by_requests
# crawl_naver_blog_by_requests("https://blog.naver.com/gangbuk_official/223177144192")# crawl_naver_blog_by_requests("https://blog.naver.com/gangbuk_official/223177144192")