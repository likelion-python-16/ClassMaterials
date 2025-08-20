
Plotly [https://plotly.com/python/](https://plotly.com/python/)

인터랙티브 시각화란?
- 데이터를 단순히 보기 좋게 표현하는 것에서 나아가,
- 사용자가 마우스로 클릭하거나, 확대/축소하고, 값을 확인할 수 있는 동적인 시각화 방식이에요.
- 예: 꺾은선 그래프 위에 마우스를 올리면 해당 값이 팝업으로 보임.

인터랙티브 시각화를 위한 Plotly 설치
```bash
pip install plotly
```

Plotly란?
- 파이썬 기반의 인터랙티브 시각화 라이브러리예요.
- `Matplotlib`, `Seaborn`처럼 정적인 이미지로 출력되는 시각화와는 달리,
- Plotly는 HTML 기반의 그래프를 만들어 브라우저에서 직접 조작할 수 있어요.

인터랙티브 꺽은선 그래프:
```python
import plotly.express as px
data = [1, 2, 3, 4, 5]

# 간단한 꺾은선 그래프 생성
fig = px.line(data, title='Simple Line Plot') 

fig.show() # 브라우저에서 인터랙티브 그래프를 보여줌
```

막대 그래프 (Bar Chart)
```python
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")

# 카테고리별 평균 급여 계산
category_salary = df.groupby("category")["salary"].mean().reset_index()

# 막대 그래프 생성
fig = px.bar(category_salary, x="category", y="salary", 
             title="카테고리별 평균 급여", 
             labels={"salary": "평균 급여", "category": "카테고리"})

fig.show()
```

산점도 (Scatter Plot)
```python
import plotly.express as px
import pandas as pd

# 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")

# 산점도 생성
fig = px.scatter(df, x="age", y="salary", color="category", 
                 hover_data=["id", "score", "on_leave"],
                 title="나이와 급여의 관계 (카테고리별 색상 구분)")

fig.show()
```

히스토그램 (Histogram)
```python
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")

fig = px.histogram(df, x="salary", nbins=30, 
                   title="전체 급여 분포", 
                   labels={"salary": "급여"})

fig.show()
```

상자그림 (Box Plot)
```python
import plotly.express as px

# 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")

fig = px.box(df, x="category", y="salary", color="category", 
             title="카테고리별 급여 분포 (Box Plot)")

fig.show()
```

버블 차트 (Bubble Chart)
```python
import plotly.express as px
df = px.data.gapminder().query("year == 2007")

fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60,
                 title="2007년 국가별 GDP vs 기대수명 (버블 크기 = 인구수)")
fig.show()
```

파이 차트 (Pie Chart)
```python
import plotly.express as px
# 데이터 불러오기
df = pd.read_csv("csv_files/employees_data.csv")

on_leave_counts = df["on_leave"].value_counts().reset_index()
on_leave_counts.columns = ["on_leave", "count"]

fig = px.pie(on_leave_counts, values="count", names="on_leave", 
             title="휴가 여부 비율")

fig.show()
```

애니메이션 (Animated Bubble Chart)
```python
import plotly.express as px
df = px.data.gapminder()

fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year",
                 animation_group="country", size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60,
                 title="연도별 전세계 GDP와 기대수명 추이")
fig.show()
```

