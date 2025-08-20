실행이 되어 있는 상태에서
```python
from sqlalchemy import create_engine
import pandas as pd

# DB 연결 엔진 (비밀번호, IP, 포트는 실제 정보로 변경)
engine = create_engine("mysql+pymysql://django_user:DjangoUserPass!123@172.20.203.81:3306/restaurant_db")
connection = engine.connect()
```

글을 생성할때는 그 테이블에 외래키가 있는지 먼저 확인해야 합니다.(restaurant)
```python
from sqlalchemy import text

# SQL 실행
query = text("SHOW COLUMNS FROM restaurant_restaurant")
result = connection.execute(query)

# Pandas로 보기 좋게 출력
df_columns = pd.DataFrame(result.fetchall(), columns=result.keys())
print(df_columns)
```

결과: 
```
         Field            Type Null  Key Default           Extra
0           id          bigint   NO  PRI    None  auto_increment
1         name    varchar(100)   NO  MUL    None                
2    anch_name    varchar(100)  YES  MUL    None                
3      address    varchar(255)   NO  MUL    None                
4      feature    varchar(255)   NO         None                
5    is_closed      tinyint(1)   NO         None                
6     latitude  decimal(16,12)   NO  MUL    None                
7    longitude  decimal(16,12)   NO  MUL    None                
8        phone     varchar(16)  YES         None                
9       rating    decimal(3,2)   NO         None                
10   ing_count    int unsigned   NO         None                
11   tart_time         time(6)  YES         None                
12    end_time         time(6)  YES         None                
13  lrder_time         time(6)  YES         None                
14   tegory_id          bigint  YES  MUL    None                
15   scription        longtext  YES         None                
16   region_id          bigint  YES  MUL    None
```
글을 생성할때 필수 입력값만 넣고, 나머지는 NULL 허용되니까 내용생략 가능합니다.


글 생성 : 필수 컬럼만 포함한 INSERT 예시 (외래키 제외 버전)
```python
from sqlalchemy import text

query = text("""
    INSERT INTO restaurant_restaurant (
        name, address, feature, is_closed,
        latitude, longitude, phone,
        rating, rating_count,
        start_time, end_time
    ) VALUES (
        :name, :address, :feature, :is_closed,
        :latitude, :longitude, :phone,
        :rating, :rating_count,
        :start_time, :end_time
    )
""")

params = {
    "name": "맛있는 김밥천국",
    "address": "서울시 강남구 테헤란로 123",
    "feature": "24시간 운영, 저렴한 가격",
    "is_closed": 0,  # 0 = 영업중, 1 = 폐업
    "latitude": 37.501274,
    "longitude": 127.039585,
    "phone": "02-123-4567",
    "rating": 4.2,
    "rating_count": 122,
    "start_time": "00:00:00",
    "end_time": "23:59:00"
}

connection.execute(query, params)
connection.commit()
```

READ: `restaurant_restaurant` 테이블 전체 불러오기
```python
query = "SELECT * FROM restaurant_restaurant;"
df = pd.read_sql(query, connection)
print(df.head())  # 데이터 일부 확인
```

UPDATE: 상점(id=2)만 이름 변경
```python
from sqlalchemy import text

update_query = text("""
    UPDATE restaurant_restaurant
    SET name = '성남_스테이크'
    WHERE id = 1;
""")
connection.execute(update_query)
connection.commit()
```

DELETE: 리뷰 평점이 1점 이하인 리뷰 삭제
```python
delete_query = """
DELETE FROM restaurant_restaurant
WHERE id = 1;
"""
connection.execute(delete_query)
connection.commit()  # ← 커밋도 꼭 해야 실제 반영됨
```

추가: 원하는 조건만 불러오기 (예: 서울 지역 맛집)
```python
df_seoul = pd.read_sql("""
SELECT * FROM restaurant_restaurant
WHERE id = 1
""", connection)

print(df_seoul)
```
- 원하는 조건: `id = 1`인 레스토랑만 조회

 테스트 테이블 만들기 (`test_table`) (필요시)
```python
create_sql = """
CREATE TABLE IF NOT EXISTS test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    A INT,
    B INT
);
"""
connection.execute(create_sql)
```

---
CREATE
```
Pandas: df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
SQL: INSERT INTO table_name (A, B) VALUES (1, 3), (2, 4);
```

READ
```
Pandas: df = pd.read_sql('SELECT * FROM table_name', connection)
SQL: SELECT * FROM table_name;
```

UPDATE
```
Pandas: df.loc[df['A'] > 1, 'B'] = 5
SQL: UPDATE table_name SET B = 5 WHERE A > 1;
```

DELETE
```
Pandas: df = df[df['A'] > 1]
SQL: DELETE FROM table_name WHERE A <= 1;
```