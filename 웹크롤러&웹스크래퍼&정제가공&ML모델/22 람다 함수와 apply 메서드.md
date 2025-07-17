Pandas에서 `apply()`와 `lambda` 함수를 사용해서 데이터를 가공하거나 계산하는 방법으로 `lambda 함수`와 `apply()` 메서드를 사용하면 Pandas에서 복잡한 조건 처리나 사용자 맞춤 데이터 변형을 쉽게 할 수 있습니다.

`lambda` 함수
- 간단한 함수를 한 줄로 표현하는 파이썬 문법
- 이름이 없는 함수라고 해서 "익명 함수"라고도 부름

`apply()` 메서드
- Pandas의 `DataFrame` 또는 `Series`에서 각 행이나 열에 함수를 적용할 수 있는 메서드
문법: Series (열)에 적용할 때(함수가 작동하도록 만드는 메서드)
```python
Series.apply(func)
```

DataFrame (전체 표)에 적용할 때:
```python
DataFrame.apply(func, axis=0 or 1)
```
- **`axis=0`** (기본값): 열(column) 단위로 함수 적용
- **`axis=1`**: 행(row) 단위로 함수 적용
- **`func`**: 각 행 또는 열에 적용할 함수

왜 apply함수와 람다함수를 함께 사용해야 하는가?
비유해서 설명하면:
`lambda x: x * 2` ← 이건 "공식"이죠.  
하지만 이걸 어디에 써야 할지, 어떻게 돌려야 할지 알려주는 게 필요해요.
그래서:
- `lambda`는 계산기 (계산 방법)
- `apply()`는 계산기를 하나하나 값에 눌러주는 사람 (함수 호출자)


✅ 실제 분석에서 자주 쓰이는 상황

나이에 따라 연령대 분류하기
```python
import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("csv_files/combined_customers.csv")

# 연령대 분류 (NaN 처리 포함)
df["age_group"] = df["age"].apply(
    lambda x: "정보없음" if pd.isnull(x) else ("성인" if x >= 20 else "청소년")
)

# 필요한 열만 추출
result = df[["customer_id", "name", "age_group"]]

# 결과 출력
print(result)
```
- 활용 목적: 마케팅, 사용자 분류, 정책 추천 등에 활용  
- 설명: 숫자(나이)를 텍스트(연령 그룹)으로 변환하고 싶을 때 사용

가입 시기(`join_date`) 기준으로 가입 연도(year) 추출하기
```python
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("csv_files/combined_customers.csv")

# 가입 연도 추출 (join_date에서 년도만 추출)
df["join_year"] = pd.to_datetime(df["join_date"]).dt.year

# 결과 출력
result = df[["customer_id", "name", "join_date", "join_year"]]
print(result)
```
- 활용 목적: 연도별 고객 가입자 수 분석, 마케팅 대상 분류, 고객 생애주기 분석 등에 활용
- 설명: 문자열 형태의 가입일(`join_date`)에서 연도만 추출하여 가입 시기를 연도 단위로 분석할 수 있도록 함

여러 열을 결합해서 새로운 열 만들기 (문자열)
```python
import pandas as pd

# CSV 불러오기 
df = pd.read_csv("csv_files/customers_with_korean_names.csv")

# "name" 열에서 성과 이름 분리 (예: 김민준 → 김, 민준)
df["last_name"] = df["name"].apply(lambda x: x[0])  # 첫 글자 = 성
df["first_name"] = df["name"].apply(lambda x: x[1:]) # 나머지 = 이름

# 다시 full_name 만들기
df["full_name"] = df["first_name"] + df["last_name"]

# 결과확인
print(df[["name", "first_name", "last_name", "full_name"]].head())
```
- 활용 목적: 성과 이름 정보를 분리하거나 재조합하여 고객 이름을 다양하게 가공·표현할 때 활용
- 설명: 기존 문자열 데이터를 나누거나 합쳐서 새로운 열(`full_name`)을 생성하는 방식으로, 데이터 가공이나 이름 포맷 변경 등에 사용

`order_amount`(주문 금액)를 기준으로 등급(grade) 을 분류하는 조건식
```python
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("csv_files/combined_orders.csv")

# 주문 금액 기준으로 등급 분류
df["grade"] = df["order_amount"].apply(
    lambda x: "A" if x >= 300 else ("B" if x >= 150 else "C")
)

# 결과 출력
print(df[["order_id", "order_amount", "grade"]].head())
```
- 활용 목적: 주문 금액에 따라 고객 또는 주문을 등급별로 분류하여 혜택 제공, 마케팅 전략 수립, 우수 고객 분석 등에 활용 
- 설명: 복잡한 if/else 조건문을 람다로 짧게 처리할 수 있음

결측값(NaN)을 대체하거나 사용자 정의 처리
```python
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("csv_files/combined_customers.csv")

df["age_label"] = df["age"].apply(
    lambda x: f"{int(x)}세" if pd.notnull(x) else "정보없음"
)

print(df[["customer_id", "age", "age_label"]].head())
```
- 활용 목적: 데이터 정제(Cleansing)  
- 설명: NaN 등 특수값을 특정 값으로 처리할 때도 사용

---
같은 결과지만 Pandas의 `apply()` 메서드와 람다 함수의 사용법을 이해하고 비교
- 두 코드는 결과값이 같습니다. 
- 하지만 함수 작성 방식에 차이가 있습니다:
	- 하나는 사용자 정의 함수 (`def`)를 먼저 정의한 뒤 `apply()`에 전달하고,  
	- 다른 하나는 익명 함수 (`lambda`)를 `apply()` 안에 직접 작성합니다.

사용자 정의 함수 (function)를 만든 후 `apply()`에 전달
```python
import pandas as pd

def doubling_age(num):
    return num * 2

df = pd.read_csv("csv_files/combined_customers.csv")
df["age_x2"] = df["age"].apply(doubling_age)
print(df)
```

익명 함수 (lambda)를 `apply()` 안에 직접 작성
```python
import pandas as pd

df = pd.read_csv("csv_files/combined_customers.csv")
df["age_x2"] = df["age"].apply(lambda x: x * 2)
print(df)
```