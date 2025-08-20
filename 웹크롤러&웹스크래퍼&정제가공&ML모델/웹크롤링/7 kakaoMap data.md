카카오맵[https://map.kakao.com/](https://map.kakao.com/)
Selenium 공식 문서 (Python)[https://www.selenium.dev/documentation/webdriver/](https://www.selenium.dev/documentation/webdriver/)

webdriver-manager 공식 문서
[https://pypi.org/project/webdriver-manager/](https://pypi.org/project/webdriver-manager/)

웹드라이버 (WebDriver): 코드로 조종할 수 있게 해주는 프로그램(중간 연결자)입니다. Selenium이 이걸 통해 브라우저를 움직여요.

![[Pasted image 20250629103057.png|200]]
폴더 및 파일생성
`__init__`파일을 폴더안에 만들어주는 이유?
`selenium_crawler` 폴더가 패키지로 인식되어야 import가 가능합니다.
`__init__.py`는 “이 폴더는 파이썬 모듈이야!” 라고 명시하는 용도입니다. 빈 파일이어도 무방해요.

공식문서에 있는 기본 뼈대 탬플릿은 다음과 같습니다:
```python
# Selenium에서 Chrome 브라우저를 제어하기 위한 웹드라이버 객체
from selenium import webdriver

# ChromeDriver 실행을 도와주는 Service 객체 
# (드라이버 경로 설정 및 실행 관리)
from selenium.webdriver.chrome.service import Service

# ChromeDriver를 자동으로 설치하고 최신 버전으로 관리해주는 도구
from webdriver_manager.chrome import ChromeDriverManager

# HTML 요소를 특정 속성(ID, CLASS 등)으로 찾기 위한 도구
from selenium.webdriver.common.by import By

# 특정 조건이 충족될 때까지 기다리기 위한 명시적 대기 기능
from selenium.webdriver.support.ui import WebDriverWait

# WebDriverWait과 함께 쓰이며, 요소가 특정 상태일 때까지 기다릴 조건을 정의 예: 요소가 화면에 보일 때까지(wait until visible)
from selenium.webdriver.support import expected_conditions as ec
# Selenium의 공식 문서 및 공식 권장 방식에 기반한 모듈들입니다.  

def crawl_example():
	driver = None
    try:
	    # 1. 드라이버 셋업
        service = Service(ChromeDriverManager().install())
	    driver = webdriver.Chrome(service=service)
		# driver는 Chrome 브라우저를 제어하는 웹드라이버 객체입니다.
		# 이 객체가 내부적으로 크롬을 켜고 
		# (ChromeDriver.exe 같은 실행파일을 통해)  
		# 우리가 .get(), .find_element() 같은 명령을 내리면 실제 
		# 브라우저에서 움직입니다.
	

        # 2. 페이지 열기
        driver.get("https://example.com")

        # 3. 요소 로딩 대기
        wait = WebDriverWait(driver, 10)
        target = wait.until(ec.presence_of_element_located((By.ID, "some-id")))

        # 4. 입력 및 동작
        target.send_keys("검색어")

        # 5. 결과 처리
        result = driver.page_source
        return result
    finally: # 에러가 나든 안나든 무조건 실행
        driver.quit()
```
except는 에러가 났을때만 실행 즉, 에러가 발생하여 except가 발생하면 driver.quit()는 실행이 안되버립니다.  그리고 브라우저가 안닫혀요. 그런 문제때문에 finally를 실행시키는데 try에서 에러가 나버릴때 finally가 실행되면서 빠져나오려면 driver = none이 빈그릇이 있어야 에러없이 빠져나올수 있습니다. 그러나 except가 없으니 에러가 왜 났는지 기록에 남지 않아요. 그래서 아래 코드를 보면 except가 추가된 코드입니다.

파일구조:
```
프로젝트/
  ├─ selenium_crawler/
  │    └─ kakaomap_scrap1.py  ← 여기 함수 정의
  ├─ cafe_data.json
  ├─ venv/
  └─ 현재 실행 중인 Jupyter Notebook (.ipynb)
```
이때 Jupyter Notebook에서 아래 코드를 실행하면:
```python
import sys, os
sys.path.append(os.getcwd())

from selenium_crawler.kakaomap_scrap1 import get_data_from_kakaomap as get_data_v1
get_data_v1()
```
`sys.path.append(os.getcwd())`가 필요한 이유는 -Jupyter Notebook은 보통 프로젝트 루트에서 실행됩니다. 하지만 내부적으로 `sys.path`에`selenium_crawler` 폴더가 포함되지 않아서,  해당 모듈을 찾지 못할 수 있습니다.
그래서 `os.getcwd()`를 통해 현재 디렉토리를 `sys.path`에 강제로 넣어주는 거죠.

파일 구조가 이렇다면:
```
프로젝트/
├─ selenium_crawler/
│   ├─ __init__.py
│   ├─ kakaomap_scrap1.py
│   ├─ kakaomap_scrap.py
│   ├─ naver_blog_scrap.py
│   └─ 현재 실행 중인 Jupyter Notebook (.ipynb)  
└─ cafe_data.json
```
이때 Jupyter Notebook에서 아래 코드를 실행하면:
```python
from kakaomap_scrap1 import get_data_from_kakaomap
get_data_from_kakaomap()
```
`selenium_crawler`는 상위 폴더니까 import 경로에 안 쓰고 그냥 같은 폴더 내의 파일 이름으로 import하면 됩니다.

그러나 가능하면 쥬피터 노트북에서 실험용으로 사용할때는 아래코드를 사용하는 것을 권장합니다. 하지만 배포코드에서는 정식 패키지 구조를 따르는 것이 좋습니다.
```python
import sys, os
sys.path.append(os.getcwd())
```
모듈 import 에러 방지 및 상대경로에서 자유로움


---
`kakaomap_scrap1.py` 코드작성
Selenium 기반 크롤링
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def get_data_from_kakaomap():
	driver = None
    try:
	    # 초기 셋업 (웹드라이버 설정)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # 호출부 (웹사이트 접속 및 초기 로딩 대기)
        driver.get("https://map.kakao.com/")
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))

        # 입력부 (검색어 입력 및 실행)
        search_input = driver.find_element(By.ID, "search.keyword.query")
        search_input.send_keys("강남구 카페")
        search_input.send_keys(Keys.ENTER)
       
        # 대기부 (검색 결과 리스트 로딩 대기)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

        # 출력부 (HTML 추출)
        place_list = driver.find_element(By.ID, "info.search.place.list")
        shop_list = place_list.get_attribute("innerHTML")

        # 종료부 (브라우저 닫기 + 반환)
        driver.quit()
        return shop_list
        
    except Exception as e:
        print(e)
        raise e # 필요 시 다시 예외 던지기
        
    finally:
        if driver:
            driver.quit() # 무조건 브라우저 닫기
```
위 코드는 웹드라이버 크롤링의 기본 구조 (템플릿)입니다. 즉, 웹드라이버로 특정 페이지에서 원하는 데이터를 가져오는 자동화 스크립트의 골격이라고 생각하면 됩니다.

필요한 모듈 임포트
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
```

드라이버 설정 및 실행
```python
driver = None
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

카카오맵 열고, 검색창이 보일 때까지 대기
```python
driver.get("https://map.kakao.com/")
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))
```

검색어 입력 및 실행
```python
search_input = driver.find_element(By.ID, "search.keyword.query")
search_input.send_keys("강남구 카페")
search_input.send_keys(Keys.ENTER)
```

결과 리스트가 뜰 때까지 대기
```python
wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))
```

결과 추출 및 확인
```python
place_list = driver.find_element(By.ID, "info.search.place.list")
shop_list = place_list.get_attribute("innerHTML")

# 결과 일부만 보기
print(shop_list[:1000])  # 너무 길면 일부만 출력
```

드라이버 종료 (무조건 마지막에 실행)
```python
if driver:
    driver.quit()
```

쥬피터 연결
```python
jupyter notebook --no-browser --port=8888
```

또는 python에 모두 입력하고 아래와 같이 실행합니다.
```python
import sys, os
sys.path.append(os.getcwd())

from selenium_crawler.kakaomap_scrap1 import get_data_from_kakaomap as get_data_v1

get_data_v1()
```
---
```python
# 입력부 (검색어 입력 및 실행)
search_input = driver.find_element(By.ID, "search.keyword.query")
search_input.send_keys("강남구 카페")
search_input.send_keys(Keys.ENTER)
```
- `By.ID`는 HTML 요소의 `id` 속성을 기준으로 요소를 찾는 방식입니다.
- `"search.keyword.query"`는 해당 입력 필드의 `id` 값입니다.
- HTML 문서 내에서 id='search.keyword.query'를 가진 `<input>` 요소를 찾기

카카오맵이 검색하는 과정을 살펴보면 input태그에서 검색어를 입력하고 엔터 또는 돋보기를 클릭한다.
- `find_element(by, value)`: `WebDriver` 또는 `WebElement` 객체의 내장 메서드로 웹 페이지에서 **단일 요소**를 찾기 위한 메서드입니다.
- `By.ID`, `By.CLASS_NAME`, `By.XPATH`, `By.CSS_SELECTOR`: 매개변수로 어떤 기준으로 요소를 찾을지 지정하는 Enum 객체
- `value`: 찾을 대상의 실제 식별값 (id, class명, XPath 표현식 등)

특수키종류
```python
from selenium.webdriver.common.keys import Keys

Keys.ENTER        # 엔터
Keys.RETURN       # 리턴 (ENTER와 동일한 경우도 있음)
Keys.TAB          # 탭 키
Keys.ESCAPE       # ESC
Keys.BACKSPACE    # 백스페이스
Keys.ARROW_DOWN   # 방향키 아래
```

---
Selenium에서 페이지가 로딩될 때까지 특정 요소가 "보일 때까지 기다리는" 코드
```python
from selenium.webdriver.support import expected_conditions as ec
```

```python
# 대기부 (검색 결과 리스트 로딩 대기)
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))
```

`visibility_of_element_located(locator)` : 조건이 참이 되는 시점까지 기다리는 함수

---
`검색 결과 전체 리스트를 감싸고 있는 <ul> 태그가 "보이게 될 때까지" 기다리는 조건`
```python
wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))
```

검색결과 확인
```python
place_list = driver.find_element(By.ID, "info.search.place.list")
shop_list = place_list.get_attribute("innerHTML")
```
`get_attribute()` : Selenium의 `WebElement` 객체에서 HTML 속성(attribute)의 값을 가져오는 메서드
`place_list` 요소 내부에 있는 HTML 코드 전체(자식들 포함)를 문자열로 가져와서 `shop_list` 변수에 저장한다.

---
```python
	return shop_list
	
except Exception as e:
	print("[ERROR 발생]", e)
	raise e
	
finally:
	if driver:
		driver.quit()
```

---
디버깅과 예외 추적을 위한 코드:
`except Exception as e:`
- 위 코드(특히 `try:` 블록 안)에서 에러가 발생하면 이 `except` 블록이 실행됩니다.
- `Exception as e`는 발생한 오류 메시지를 `e`라는 변수에 저장합니다.

`print("[ERROR 발생]", e)`
- 예외 객체 `e`를 출력합니다.
- 콘솔이나 로그에 어떤 에러가 났는지 확인할 수 있도록 도와줍니다.

`raise e`
- 에러를 다시 바깥으로 던짐(재전파)합니다.
- 단순히 에러를 무시하지 않고, 이 함수가 호출된 상위 코드에게 "에러가 났다"고 알림으로 역할은 호출자에게 에러를 알리기 위한 재전파

`finally:` 
- 무조건 실행하므로 try에서 에러가 나도 브라우저를 닫을수 있습니다.

---
의사코드:
```python
# Selenium을 사용한 웹 크롤링 코드
# 카카오맵에서 "강남구 카페"를 검색하고, 결과 HTML 코드를 가져오는 함수

# 크롬 브라우저를 자동으로 열고 조작하기 위한 모듈
from selenium import webdriver 

# 드라이버 서비스 설정용
from selenium.webdriver.chrome.service import Service 

# 크롬 드라이버를 자동 설치해주는 라이브러리
from webdriver_manager.chrome import ChromeDriverManager  

# 실행 중간에 잠깐 멈추는 기능
from time import sleep

# 요소를 찾을 때 id, class 등 기준을 정할 수 있게 함
from selenium.webdriver.common.by import By

# 키보드 입력 (예: 엔터키) 처리용
from selenium.webdriver.common.keys import Keys 

# 최대 몇 초까지 기다릴지를 설정하는 기능
from selenium.webdriver.support.ui import WebDriverWait 

# 기다리는 조건을 정의하는 도구
from selenium.webdriver.support import expected_conditions as ec  

# 크롤링을 실행하는 함수 정의
def get_data_from_kakaomap():
    try:
        # 크롬 드라이버 자동 설치 및 실행을 위한 설정
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # 크롬 브라우저로 카카오맵 웹사이트 열기
        driver.get("https://map.kakao.com/")

# 최대 10초 동안 특정 요소(검색창)가 나타날 때까지 기다릴 수 있도록 설정
        wait = WebDriverWait(driver, 10)

# id가 "search.keyword.query"인 검색창이 화면에 보일 때까지 대기
        wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))

        # 검색창 요소를 찾음
        search_input = driver.find_element(By.ID, "search.keyword.query")

        # 검색창에 "강남구 카페" 라는 텍스트 입력
        search_input.send_keys("강남구 카페")

        # 키보드의 Enter 키를 눌러 검색을 실행
        search_input.send_keys(Keys.ENTER)

        # 검색 결과 리스트가 나타날 때까지 다시 최대 10초 대기
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

        # 검색 결과가 담긴 요소를 찾음
        place_list = driver.find_element(By.ID, "info.search.place.list")

        # 해당 요소의 HTML 코드를 가져옴 (여러 가게 목록이 포함됨)
        shop_list = place_list.get_attribute("innerHTML")

        # 브라우저 종료 (크롬 창 닫기)
        driver.quit()

        # 수집한 HTML 코드 반환
        return shop_list

    # 오류 발생 시 에러 메시지를 출력하고 예외로 넘김
    except Exception as e:
        print(e)
        raise e

```

| 파트                | 설명                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------ |
| 함수 정의             | `def get_data_from_kakaomap():`, `def get_items(...):`와 같은 함수는 파이썬 함수 문법입니다. (기초 문법) |
| Selenium 사용법      | 웹 브라우저 자동화를 위한 라이브러리입니다. 사용자가 마우스로 하는 일을 코드로 자동화함                                    |
| BeautifulSoup 사용법 | 웹 페이지 HTML을 파싱해서 원하는 정보를 추출하는 데 사용됩니다. 즉, 데이터 "긁기" 역할                                |

Jupyter notebook 실행:
```bash
jupyter notebook --no-browser --port=8888
```

연동된 Jupyter notebook에 kakaomap1.ipynb에 작성후 실행
```python
import sys, os
sys.path.append(os.getcwd())

from selenium_crawler.kakaomap_scrap1 import get_data_from_kakaomap as get_data_v1

get_data_v1()
```

의사코드:
```python
# 현재 작업 중인 디렉토리 경로를 시스템 경로(sys.path)에 추가하여
# 해당 폴더 안에 있는 모듈(파이썬 파일)을 불러올 수 있도록 설정함
import sys, os
sys.path.append(os.getcwd())  
# 현재 작업 디렉토리 경로를 Python 모듈 검색 경로에 추가

# selenium_crawler라는 폴더(패키지) 안에 있는 kakaomap_scrap1.py 파일에서 get_data_from_kakaomap 함수를 불러오되, 이름을 get_data_v1으로 바꿔 사용하겠다는 뜻
from selenium_crawler.kakaomap_scrap1 import get_data_from_kakaomap as get_data_v1

# 위에서 불러온 함수(get_data_v1)를 실제로 실행함
# 강남구 카페 정보를 크롤링하고, 결과(html 또는 dict)를 반환함
get_data_v1()
```
---
kakaomap_scrap.py 수정
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

  
def get_data_from_kakaomap():
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # 웹사이트 열기
        driver.get("https://map.kakao.com/")
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "search.keyword.query")))

        # 검색창에 검색어 입력하기
        search_input = driver.find_element(By.ID, "search.keyword.query")
        # wait until the element is visible
        search_input.send_keys("강남구 카페")
        search_input.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)

        wait.until(ec.element_to_be_clickable((By.ID, "info.search.place.more")))
        driver.execute_script("""
        var element = document.getElementById('dimmedLayer');
        if (element) {
            element.className = 'DimmedLayer HIDDEN';
        }
        """)

        sleep(1)
        show_more_btn = driver.find_element(By.ID, "info.search.place.more")
        show_more_btn.click()

        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.page")))

        page_count = 0
        items = []

        while page_count <= 5:
            if page_count != 0 and page_count % 5 == 0:
                page_next_btn_id = "info.search.page.next"
                next_btn = driver.find_element(By.ID, page_next_btn_id)
                next_btn.click()
                wait = WebDriverWait(driver, 10)              wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

            page_count += 1
            page_num = page_count % 5 if page_count % 5 != 0 else 5
            page_btn_id = f"info.search.page.no{page_num}"
            next_btn = driver.find_element(By.ID, page_btn_id)
            next_btn.click()
            wait = WebDriverWait(driver, 10)           wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

            place_list = driver.find_element(By.ID, "info.search.place.list")
            shop_list = place_list.get_attribute("innerHTML")

            get_items(shop_list, items)
            sleep(2)
        # 검색 결과 확인
        
        driver.quit()
        return items
    except Exception as e:
        print(e)
        raise e

def get_items(html: str, parsed_items: list):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.PlaceItem.clickArea")
    for item in items:
        item_dict = {}
        item_dict["name"] = item.find('span', {'data-id': 'screenOutName'}).text
        item_dict["score"] = item.find('em', {'data-id': 'scoreNum'}).text
        item_dict["address"] = item.find('p', {'data-id': 'address'}).text
        item_dict["hour"] = item.find('a', {'data-id': 'periodTxt'}).text
        parsed_items.append(item_dict)

    return parsed_items
```
---
```python
from time import sleep

# "더보기" 버튼이 로드될 때까지 대기
wait = WebDriverWait(driver, 10)
wait.until(ec.element_to_be_clickable((By.ID, "info.search.place.more")))
```
`"더보기"` 버튼이 완전히 로딩되고 클릭 가능할 때까지 기다림
검색 결과가 1페이지 이상일 경우, "더보기"를 눌러야 페이지네이션이 나타남

---
```python
# 검은 화면(딤드 레이어)이 뜬 경우 강제로 숨김 (중요!)
driver.execute_script("""
var element = document.getElementById('dimmedLayer');
if (element) {
    element.className = 'DimmedLayer HIDDEN';
}
""")
sleep(1)
```
`var`는 Selenium이 JS를 DOM의 루트에서 실행할 때 더 호환성이 좋음


---
```python
# "더보기" 버튼 클릭 → 페이지네이션 노출 유도
show_more_btn = driver.find_element(By.ID, "info.search.place.more")
show_more_btn.click()
```
클릭 메서드

---
```python
# 페이지네이션 영역이 보일 때까지 대기
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "info.search.page")))
```
---
```python
# 페이지 넘기며 반복 수집 (1~6페이지)
page_count = 0
items = []

while page_count <= 5:
    if page_count != 0 and page_count % 5 == 0:
        page_next_btn_id = "info.search.page.next"
        next_btn = driver.find_element(By.ID, page_next_btn_id)
        next_btn.click()
        wait = WebDriverWait(driver, 10)
        wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

    page_count += 1
    page_num = page_count % 5 if page_count % 5 != 0 else 5
    page_btn_id = f"info.search.page.no{page_num}"

    next_btn = driver.find_element(By.ID, page_btn_id)
    next_btn.click()
    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))

    place_list = driver.find_element(By.ID, "info.search.place.list")
    shop_list = place_list.get_attribute("innerHTML")

    get_items(shop_list, items)
    sleep(2)
```


검색 결과 페이지를 1페이지부터 6페이지까지 반복하면서 데이터를 수집하는 코드

반복 시작 전 초기화
```python
page_count = 0   # 현재 몇 번째 페이지를 수집 중인지 추적하는 변수 (0부터 시작)
items = []       # 모든 카페 데이터를 담을 빈 리스트
```
---
while 반복문
```python
while page_count <= 5:  # 0~5까지 총 6페이지를 수집하겠다는 의미
```
---
5페이지 단위로 "다음" 버튼 클릭 처리
```python
if page_count != 0 and page_count % 5 == 0:
```
5페이지마다 한 번씩 "다음" 버튼을 눌러야 함
카카오맵은 5페이지 단위로 페이지 그룹이 나뉘니까 필요.
5의 배수이므로 5마다 0이 나옵니다. 5,10,15,20...

---
```python
page_next_btn_id = "info.search.page.next"
next_btn = driver.find_element(By.ID, page_next_btn_id)
next_btn.click()  # "다음 >" 버튼 클릭
```
페이지 넘김을 위해 "다음" 버튼(`id="info.search.page.next"`) 클릭

---
```python
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))
```
새 페이지가 로드될 때까지 기다림

---
```python
page_count += 1  # 수집한 페이지 수를 1 증가
```
페이지 수 증가

---
현재 클릭할 페이지 버튼 ID 설정
```python
page_num = page_count % 5 if page_count % 5 != 0 else 5
```
- 현재 페이지 번호에 해당하는 버튼은 `info.search.page.no1`, `no2`, ..., `no5`
- 예외 처리: 5의 배수일 때는 `0`이 되므로 `5`로 바꿔줌

1~5페이지 구간
```
<a id="info.search.page.no1">1</a>
<a id="info.search.page.no2">2</a>
<a id="info.search.page.no3">3</a>
<a id="info.search.page.no4">4</a>
<a id="info.search.page.no5">5</a>
```

6~10페이지 구간 (다음 클릭하면 바뀜)
```
<a id="info.search.page.no1">6</a>
<a id="info.search.page.no2">7</a>
<a id="info.search.page.no3">8</a>
<a id="info.search.page.no4">9</a>
<a id="info.search.page.no5">10</a>
```
즉, id는 `no1` `no5` 그대로고, 텍스트만 6 ~10으로 바뀜

`page_num = page_count % 5 if page_count % 5 != 0 else 5`
5의 배수일 때 
`"5로 나눈 나머지가 0이 아니라면"` → 나머지 그대로 (`1~4`)
`"나머지가 0이면"` → `5`라고 치환

---
```python
page_btn_id = f"info.search.page.no{page_num}"  
# 예: info.search.page.no3
```
클릭할 페이지 번호의 ID 문자열 생성

---
```python
next_btn = driver.find_element(By.ID, page_btn_id)
next_btn.click()
```
해당 페이지 번호 버튼을 찾아 클릭 (예: 2페이지 클릭)

---
```python
wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "info.search.place.list")))
```
페이지가 바뀐 뒤, 장소 목록이 다시 로딩될 때까지 기다림

---
```python
place_list = driver.find_element(By.ID, "info.search.place.list")
shop_list = place_list.get_attribute("innerHTML")
```
`<ul id="info.search.place.list">` 내부의 HTML만 문자열로 가져옴

---
BeautifulSoup으로 HTML 파싱 후 items에 저장
```python
get_items(shop_list, items)
```
- `get_items()` 함수로 HTML 내부 `<li>` 태그에서 이름, 평점, 주소 등 추출
- 결과를 `items` 리스트에 누적 저장

---
페이지 간 sleep
```python
sleep(2)  # 너무 빠르게 넘어가면 서버 차단 가능성 있음 → 살짝 쉬어줌
```
---
```python
def get_items(html: str, parsed_items: list):
    from bs4 import BeautifulSoup
    
    # HTML 파싱 준비
    soup = BeautifulSoup(html, "html.parser")
    
    # 가게 항목 리스트 선택
    items = soup.select("li.PlaceItem.clickArea")
    
    for item in items:
        item_dict = {}
        # 가게명
        item_dict["name"] = item.find('span', {'data-id': 'screenOutName'}).text
        # 평점
        item_dict["score"] = item.find('em', {'data-id': 'scoreNum'}).text
        # 주소
        item_dict["address"] = item.find('p', {'data-id': 'address'}).text
        # 영업시간
        item_dict["hour"] = item.find('a', {'data-id': 'periodTxt'}).text
        
        # 하나의 dict를 전체 리스트에 추가
        parsed_items.append(item_dict)

    return parsed_items
```
---
```python
def get_items(html: str, parsed_items: list):
```
- `html`: 크롤링한 `ul` 태그의 내부 HTML (`innerHTML`) 문자열
- `parsed_items`: 파싱한 결과를 저장할 리스트 (`list[dict]` 형태)
- HTML에서 카페 이름, 평점, 주소, 영업시간 등을 추출해서 `parsed_items`에 하나씩 딕셔너리로 추가함
---
BeautifulSoup로 HTML 파싱
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
```
- `html.parser`는 파이썬 내장 HTML 파서
- HTML 문자열을 BeautifulSoup 객체로 바꿔서 태그 탐색이 가능하게 만듦

---
카페 항목 리스트 찾기
```python
items = soup.select("li.PlaceItem.clickArea")
```
- `li.PlaceItem.clickArea`는:
    - `<li>` 태그인데
    - `class="PlaceItem clickArea"`를 가진 요소
- 이 한 줄로 카카오맵에 표시된 카페 하나하나의 리스트 항목들을 전부 선택함
- `items`는 각 카페를 나타내는 BeautifulSoup 객체들의 리스트

---
각 카페 항목을 하나씩 순회
```python
for item in items:
    item_dict = {}
```
- `item`: 카페 하나에 해당하는 `<li>` 요소
- `item_dict`: 한 카페의 정보(name, score, address, hour)를 담을 딕셔너리

---
카페명 추출
```python
item_dict["name"] = item.find("span", {"data-id": "screenOutName"}).text
```
- `<span data-id="screenOutName">카페이름</span>`에서 텍스트만 추출
- `카페 이름`이 들어가는 위치

---
평점 추출
```python
item_dict["score"] = item.find("em", {"data-id": "scoreNum"}).text
```
- `<em data-id="scoreNum">4.3</em>` 등에서 평점 숫자만 가져옴

---
주소 추출
```python
item_dict["address"] = item.find("p", {"data-id": "address"}).text
```
`<p data-id="address">서울 강남구 ...</p>` 에서 주소 텍스트 가져옴

---
영업시간 추출
```python
item_dict["hour"] = item.find("a", {"data-id": "periodTxt"}).text
```
`<a data-id="periodTxt">09:00 - 22:00</a>`처럼 영업시간 정보 추출

---
전체 결과 누적 저장
```python
parsed_items.append(item_dict)
```
- 만들어진 딕셔너리를 최종 리스트(`parsed_items`)에 추가

---
결과 리턴
```python
return parsed_items
```
모든 카페 정보를 담은 리스트를 반환

---

연동된 Jupyter notebook에 kakaomap.ipynb에 작성후 실행
```python
import sys, os
sys.path.append(os.getcwd())

from selenium_crawler.kakaomap_scrap import get_data_from_kakaomap as get_data_v2

get_data_v2()
```

