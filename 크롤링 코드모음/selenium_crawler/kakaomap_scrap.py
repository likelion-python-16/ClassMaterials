from time import sleep

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

        # 카카오 지도 웹사이트 열기
        driver.get("https://map.kakao.com/")
        wait = WebDriverWait(driver, 10)
        # 검색창이 뜰 때까지 대기
        wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))

        # 검색창에 키워드 입력
        search_input = driver.find_element(By.ID, "search.keyword.query")
        search_input.send_keys("강남구 카페")
        search_input.send_keys(Keys.ENTER)

        # "더보기" 버튼이 로드될 때까지 대기
        wait = WebDriverWait(driver, 10) #추가됨
        wait.until(ec.element_to_be_clickable((By.ID, "info.search.place.more")))
        

        #----------------추가-------------------------------------------------------
        # 가끔 뜨는 검은 화면(딤드 레이어) 숨기기 (JS 실행)
        driver.execute_script(
        """
        var element = document.getElementById('dimmedLayer');
        if (element) {
            element.className = 'DimmedLayer HIDDEN';
        }
        """
        )

        sleep(1)

        # "더보기" 버튼 클릭 → 페이지네이션 버튼 노출되도록(장소더보기 페이지네이션 보이게 하는 버튼)
        show_more_btn = driver.find_element(By.ID, "info.search.place.more")
        show_more_btn.click()

        # 페이지네이션 영역 로딩 대기
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.page")))

        # 페이지 수를 세면서 반복 진행
        page_count = 0
        items = []

        # 최대 6페이지까지 반복 크롤링
        while page_count <= 5: # 0, 1, 2, 3, 4, 5  → 총 6번 반복!
            if page_count != 0 and page_count % 5 == 0: # 페이지 수가 0이 아니고, 5의 배수일 때만 실행해라.
               # 5페이지마다 한 번씩 "다음" 버튼을 눌러야 함
               # 카카오맵은 5페이지 단위로 페이지 그룹이 나뉘니까 필요.
               # 5의 배수이므로 5마다 0이 나옵니다. 5,10,15,20...     
               

                page_next_btn_id = "info.search.page.next"
                next_btn = driver.find_element(By.ID, page_next_btn_id)
                next_btn.click()
                # 페이지 넘김을 위해 "다음" 버튼(`id="info.search.page.next"`) 클릭


                wait = WebDriverWait(driver, 10) # 새 페이지가 로드될 때까지 기다림
                wait.until(
                    ec.visibility_of_element_located((By.ID, "info.search.place.list"))
                )

            page_count += 1 # # 수집한 페이지 수를 1 증가
            page_num = page_count % 5 if page_count % 5 != 0 else 5
            page_btn_id = f"info.search.page.no{page_num}"

            # 페이지 버튼 클릭
            next_btn = driver.find_element(By.ID, page_btn_id)
            next_btn.click()
            wait = WebDriverWait(driver, 10)
            wait.until(
                ec.visibility_of_element_located((By.ID, "info.search.place.list"))
            )

            # ---------------기존코드----------------------------
            # 장소 목록 HTML 가져오기
            place_list = driver.find_element(By.ID, "info.search.place.list")
            shop_list = place_list.get_attribute("innerHTML")
             # ---------------기존코드----------------------------

            # 검색 결과 확인
            # HTML을 파싱해서 items 리스트에 추가
            get_items(shop_list, items)
            sleep(2) # sleep과 await는 모두 일시적으로 “기다린다”는 공통점이 있지만, 동작 방식은 완전히 다릅니다.
            # sleep(2) 프로그램을 2초 동안 "멈춤" "2초 동안 그냥 쉬고 아무것도 하지 마"
            # await asyncio.sleep(2) "2초 쉬는 동안, 다른 작업 먼저 해봐"
            # 2초동안 멈추게 하는 이유는 Selenium이 너무 빨리 실행되면 아직 처리가 안되서 에러가 발생할수도 있으니 기다려주게 하는겁니다.

        

#-----------기존코드------------------------------
        # 드라이버 종료 및 결과 반환
        return items
    
    except Exception as e:
        print("[ERROR]",e)
        raise e
    
    finally:
        if driver:
            driver.quit()
#-----------기존코드------------------------------            

# HTML 내부에서 카페 정보를 추출하는 보조 함수
def get_items(html: str, parsed_items: list):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.PlaceItem.clickArea")
    for item in items:
        item_dict = {}
        item_dict["name"] = item.find("span", {"data-id": "screenOutName"}).text 
        # 딕셔너리 키값인 name은 개발자가 붙여준 이름이며 나중에 모델 필드명과 같게 해주면 찾기 쉬움

        item_dict["score"] = item.find("em", {"data-id": "scoreNum"}).text
        item_dict["address"] = item.find("p", {"data-id": "address"}).text
        item_dict["hour"] = item.find("a", {"data-id": "periodTxt"}).text
        parsed_items.append(item_dict)

    return parsed_items

# py에서는 프린트문이 없어서 실행되지 않고 쥬피터내부에 print문이 있어서 출력될수 있음