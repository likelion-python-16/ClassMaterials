from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# 데이터 수집 메인 함수
def get_data_from_kakaomap():
    driver = None
    try:
        # 드라이버 셋업 (자동으로 크롬드라이버 설치)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # 웹사이트 열기
        driver.get("https://map.kakao.com/")
        wait = WebDriverWait(driver, 10)
        # 검색창이 뜰 때까지 대기
        wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))

        # 검색창에 키워드 입력
        search_input = driver.find_element(By.ID, "search.keyword.query")
        search_input.send_keys("강남구 카페")
        search_input.send_keys(Keys.ENTER)
        
        # 검색 결과 전체 리스트를 감싸고 있는 <ul> 태그가 "보이게 될 때까지" 기다리는 조건
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list"))) 
        #데이터가 있는 위치

        # 검색 결과 확인
        place_list = driver.find_element(By.ID, "info.search.place.list")
        shop_list = place_list.get_attribute("innerHTML")

        # scroll down to the bottom
        return shop_list

    except Exception as e:
        print("[ERROR 발생]", e)
        raise e
    
    finally:
        if driver:
            driver.quit()
