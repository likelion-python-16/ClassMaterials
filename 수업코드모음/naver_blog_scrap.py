import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# 텍스트에서 비가시 문자 제거 및 공백 정리 함수
def clean_text(text):
    printable = "".join(ct for ct in text if ct.isprintable())  #
    # text = re.sbu(r"[\t\n\r\f\v]+","", text) #
    cleaned = " ".join(printable.split())
    return cleaned


# 1. Selenium을 사용하여 네이버 블로그 본문을 추출하는 함수 (iframe 대응)
def crawl_naver_blog(url):
    # ChromeOptions 생성
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())

    # webdriver.Chrome()에 전달
    driver = webdriver.Chrome(
        service=service,
    )
    driver.get(url)

    iframe_element = driver.find_element(By.ID, "mainFrame")
    driver.switch_to.frame(iframe_element)
    driver.find_element(By.ID, "post-area")
    res = driver.page_source
    driver.quit()

    soup = BeautifulSoup(res, "html.parser")
    content = soup.find("div", {"class": "se-main-container"})
    if content is None:
        content = soup.find("div", {"id": "post-area"})
    if content is None:
        raise RuntimeError("본문 컨테이너를 찾을 수 없습니다.")

    raw = content.get_text(separator="")
    cleande_content = clean_text(raw)
    return cleande_content


# 2. requests만 사용하여 네이버 블로그 본문을 추출하는 함수 (iframe 수동 처리)
def crawl_naver_blog_by_requests(url):
    res = requests.get(url)
    root_url = "https://blog.naver.com"

    if "id='mainFrame'" in res.text:
        soup = BeautifulSoup(res.text, "html.parser")
        iframe = soup.find("iframe", {"id": "mainFrame"})  # iframe태그명
        iframe_src = iframe["src"]
        res = requests.get(root_url + iframe_src)

    soup = BeautifulSoup(res.text, "html.parser")
    content = soup.find("div", {"class": "se-main-container"})
    if content is None:
        content = soup.find("div", {"id": "post-area"})
    if content is None:
        raise RuntimeError("본문 컨테이너를 찾을 수 없습니다. HTML 구조를 확인하세요.")

    raw = content.get_text(separator="")
    cleande_content = clean_text(raw)
    return cleande_content


# 3. 지역 + 키워드로 네이버 블로그 리뷰 목록을 수집하는 함수
def find_reivew_article(location: str, keyword: str):
    # 1) 네이버 블로그 리뷰 검색 URL 생성
    url = (
        "https://search.naver.com/search.naver"
        "?sm=tab_hty.top&ssc=tab.blog.all"
        f"&query={location}+{keyword}+리뷰"
    )

    # 2) 요청 & 파싱
    res = requests.get(url)
    # res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # 3) 링크 추출 (soup.find_all)
    title_links = soup.find_all("a", {"class": "title_link"})
    review_list = []

    # 4) 제목에 키워드가 포함된 항목만 (title, href) 튜플로 수집
    for a in title_links:
        title = a.get_text(strip=True)
        href = a.get("href")
        if keyword in title:
            review_list.append((title, href))

    return review_list
