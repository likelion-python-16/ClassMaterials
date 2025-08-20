고급 SQL 쿼리와 Pandas 함수
	고급 SQL 쿼리와 Pandas 함수는 각각 데이터베이스 추출과 파이썬 기반 데이터 분석에 최적화되어 있습니다.  
	많은 분석가들이 SQL로 데이터를 가져오고, Pandas로 가공·분석하는 방식으로 함께 활용합니다. SQL문과 Pandas를 1:1 비교해는 방법을 알아봅니다.


SubQuery (서브쿼리, 하위 쿼리)
	특정 조건을 만족하는 데이터를 먼저 뽑고, 그걸 이용해 다시 조회하는 방식
SQL:
```python
SELECT * FROM table1 
WHERE id IN (SELECT id FROM table2 WHERE condition);
```

Pandas:
```python
subquery = df2[df2['condition']]['id']
result = df1[df1['id'].isin(subquery)]
```
---
Aggregation (집계 함수)
SQL:
```python
SELECT category, AVG(salary) 
FROM employees 
GROUP BY category;
```

Pandas:
```python
df.groupby('category')['salary'].mean()
```

###### 주요 집계 함수 비교
|목적|SQL 예시|Pandas 예시|
|---|---|---|
|평균|`AVG(column)`|`df['column'].mean()`|
|합계|`SUM(column)`|`df['column'].sum()`|
|최소값|`MIN(column)`|`df['column'].min()`|
|최대값|`MAX(column)`|`df['column'].max()`|
|개수 세기|`COUNT(column)`|`df['column'].count()`|

---
Window Functions (윈도우 함수)
	윈도우 함수(Window Function)란, 전체 데이터 중 일부 범위(= 윈도우)를 지정하고,  그 범위 안에서 누적합, 순위, 평균 등 계산을 하는 SQL 함수입니다.

1. 순위 매기기 (Ranking)
SQL:
```python
SELECT salary, RANK() OVER (ORDER BY salary) 
FROM employees;
```

Pandas:
```python
df['salary_rank'] = df['salary'].rank()
```
---
2. 이동 평균 (Moving Average)
	일정한 기간 동안의 평균을 계속 계산해 나가는 방식
SQL:
```python
SELECT AVG(salary) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
```

Pandas:
```python
df['moving_avg'] = df['salary'].rolling(window=3).mean()
```
---
3. 누적 합계 (Cumulative Sum)
	처음부터 지금까지 계속 더한 값
SQL:
```python
SELECT SUM(salary) OVER (ORDER BY salary)
```

Pandas:
```python
df['cum_salary'] = df['salary'].expanding().sum()
```
---
4. 행 번호 붙이기 (Row Number)
	각 행에 번호를 순서대로 붙이는 기능
SQL:
```python
SELECT ROW_NUMBER() OVER (ORDER BY salary) 
FROM employees;
```

Pandas:
```python
df['row_num'] = df.groupby([]).cumcount() + 1
```
---
간단한 실습해보기:

전체 평균 급여보다 높은 직원 조회
SQL:
```python
SELECT *
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

Pandas:
```python
import pandas as pd

df = pd.read_csv("csv_files/employees_data.csv")
avg_salary = df['salary'].mean()
print(avg_salary)


subquery_df = df[df['salary'] > avg_salary]
print(subquery_df)
```

---
카테고리별 평균 급여 계산
SQL:
```python
SELECT category, AVG(salary) AS avg_salary
FROM employees
GROUP BY category;
```

Pandas:
```python
import pandas as pd

df = pd.read_csv("csv_files/employees_data.csv")
avg_salary_by_category = df.groupby('category')['salary'].mean()
print(avg_salary_by_category)
```

jupyter notebook
```python
# 1. 필요한 모듈 불러오기
import pandas as pd
import sqlite3  # 간편한 임베디드 SQL DB

# 2. CSV 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")
print("원본 데이터")
print(df)

# 3. Pandas로 그룹별 평균 급여 계산(sql과 동일한 결과)
avg_salary_by_category = df.groupby('category')['salary'].mean()
print("\n Pandas 결과 (카테고리별 평균 급여):")
print(avg_salary_by_category)

# 4. SQLite 메모리 DB에 데이터 저장
conn = sqlite3.connect(":memory:")  # 임시 SQL DB
df.to_sql("employees", conn, index=False)

# 5. SQL로 그룹별 평균 급여 계산(pandas와 동일한 결과)
sql_query = """
SELECT category, AVG(salary) AS avg_salary
FROM employees
GROUP BY category;
"""
avg_salary_sql = pd.read_sql(sql_query, conn)

print("\n SQL 결과:")
print(avg_salary_sql)

# 6. DB 연결 종료
conn.close()
```

Pandas + SQLite 연동 코드:
```python
conn = sqlite3.connect(":memory:")  
df.to_sql("employees", conn, index=False)
```
- `sqlite3`는 파이썬 내장 SQL 데이터베이스 모듈입니다.
- `":memory:"`는 실제 파일을 만들지 않고 메모리(램)에만 존재하는 가상의 임시 DB를 의미해요.
- 즉, 프로그램이 실행되는 동안만 살아 있고, 종료하면 사라집니다.
- ✔️ 장점: 빠르고, 임시 테스트용으로 아주 좋음

---
급여 기준 누적 평균 계산 (Running Average)
SQL (윈도우 함수 사용):
```python
SELECT id, salary,
       AVG(salary) OVER (ORDER BY id) AS running_avg_salary
FROM employees;
```

Pandas:
```python
import pandas as pd

df = pd.read_csv("csv_files/employees_data.csv")
df['running_avg_salary'] = df['salary'].expanding().mean()
print(df)
```
`expanding()`는 처음 행부터 현재 행까지의 누적 범위(Window) 를 정의하는 메서드


jupyter notebook
```python
# 1. 모듈 불러오기
import pandas as pd
import sqlite3

# 2. employees_data.csv 파일 읽기
df = pd.read_csv("csv_files/employees_data.csv")

print(" 원본 데이터:")
print(df)

# 3. Pandas 방식: 누적 평균 (원래 순서 기준)
df_pandas = df.copy()
df_pandas['running_avg_salary'] = df_pandas['salary'].expanding().mean()

print("\n Pandas 누적 평균 결과:")
print(df_pandas[['id', 'salary', 'running_avg_salary']])

# 4. SQLite 메모리 DB에 저장
conn = sqlite3.connect(":memory:")
df.to_sql("employees", conn, index=False)

# 5. SQL 쿼리: 윈도우 함수로 누적 평균
sql_query = """
SELECT id, salary,
       AVG(salary) OVER (ORDER BY id) AS running_avg_salary
FROM employees;
"""

df_sql = pd.read_sql(sql_query, conn)

print("\n SQL 윈도우 함수 결과:")
print(df_sql)

conn.close()
```
