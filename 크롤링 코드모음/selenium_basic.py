from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1. 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 2. 웹사이트 열기
driver.get("https://www.google.com")

# 3. 검색창 찾기
search_box = driver.find_element(By.NAME, "q")  # name="q"인 요소가 검색창

# 4. 검색어 입력하고 Enter
search_box.send_keys("파이썬")
search_box.send_keys(Keys.RETURN)

# 5. 결과 대기 및 출력
time.sleep(3)
print("페이지 제목:", driver.title)

# 6. 브라우저 종료
driver.quit()

# 브라우저 실행
# :webdriver.Chrome(...)자동으로 Chrome 창 실행

# 페이지 열기
# :driver.get(URL)주소 입력 후 접속

# 요소 찾기
# :find_element(By.속성, "값")ex:ID,NAME,CLASS 등으로 요소 선택

# 입력하기:
# .send_keys("내용")텍스트 입력 또는 키보드 이벤트 전송

# 클릭하기:
# .click()버튼이나 링크 클릭

# 대기:
# time.sleep(초)페이지 로딩 기다림 (기본적인 방법)

# 종료:
# driver.quit()브라우저 닫기