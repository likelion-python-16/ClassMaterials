Pandas가 데이터를 읽을 수 있는 위치
- 📂 클라우드 저장소: 예를 들어 Google Drive, AWS S3, Dropbox 같은 곳에 저장된 파일
- 🗄️ 데이터베이스: MySQL, PostgreSQL, SQLite 같은 전문적인 데이터 저장 시스템
    
즉, Pandas는 파일뿐만 아니라 원격 서버나 데이터베이스에서도 데이터를 가져올 수 있어요.

SQL이란? (Structured Query Language)
- SQL은 데이터베이스에서 데이터를 다루기 위한 표준 언어예요.
- 주로 다음과 같은 일을 할 수 있어요:
    - 데이터를 조회하기 (ex: 30대 고객만 보기)
    - 데이터를 추가하기 (ex: 새 고객 등록)
    - 데이터를 수정하기 (ex: 이름 변경)
    - 데이터를 삭제하기 (ex: 탈퇴 고객 제거)

그리고 SQL은 복잡한 조건으로 데이터를 뽑거나, 아주 큰 데이터도 빠르게 처리할 수 있어요.

🔁 SQL과 Pandas는 서로 연결될 수 있어요
- SQL → Pandas DataFrame
    - SQL에서 데이터를 읽어서 Pandas로 가져올 수 있어요.
    - 예: `SELECT * FROM orders;` → `pd.read_sql(...)`
        
- Pandas DataFrame → SQL
    - Pandas에서 정리한 데이터를 SQL 데이터베이스에 저장할 수도 있어요.
    - 예: `df.to_sql(...)`을 이용해서 테이블로 저장

터미널에 설치:
```bash
pip install pymysql 
pip install sqlalchemy
```
`PyMySQL`은 파이썬에서 MySQL 데이터베이스에 접속할 수 있게 해주는 라이브러리
`SQLAlchemy`는 파이썬과 데이터베이스를 연결해주는 고급 도구


WSL2 환경이면, IP 바뀌었는지 확인
```
ip addr | grep inet
```
`WSL2`에서는 리눅스 쪽의 내부 IP가 재부팅할 때마다 바뀌기 때문에,  
이전과 다른 IP로 바뀌었는지를 직접 확인해야 할 때가 많습니다.

결과 예시:
```bash
inet 127.0.0.1/8 scope host lo
inet 172.20.203.81/20 brd 172.20.207.255 scope global eth0
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
```
여기서 진짜 WSL의 내부 IP는 `eth0`에 있는 이 부분이에요:
```bash
inet 172.20.203.81/20 scope global eth0
```
즉, 이 경우 IP는 → `172.20.203.81`


Jupyter Notebook (또는 Python 스크립트) 에서 사용할 수 있는 SQLAlchemy 기반의 MySQL 연결 코드
```python
from sqlalchemy import create_engine
import pandas as pd

# 접속 정보 입력
import pandas as pd
from sqlalchemy import create_engine

# SQLAlchemy 엔진 생성
# MySQL 데이터베이스에 연결할 수 있는 **엔진 객체**를 만드는 명령
engine = create_engine("mysql+pymysql://django_user:DjangoUserPass!123@172.20.203.81:3306/restaurant_db")

# 접속
connection = engine.connect()

# restaurant_restaurant 테이블의 모든 데이터를 선택(select)해라
query = "SELECT * FROM restaurant_restaurant;"

# 데이터프레임으로 불러오기
df = pd.read_sql(query, connection)

# 결과 확인
print(df.head())
```

SQLAlchemy 엔진(`Engine`)은 파이썬 코드와 데이터베이스(DB) 사이를 연결해주는 "다리(bridge)" 역할을 합니다.
즉, SQLAlchemy 엔진은 데이터베이스와의 연결(커넥션)을 생성하고 관리해주는 객체입니다.


SQL 쿼리문(SQL Query)
`SELECT`	
- 데이터를 가져오겠다는 명령
`*`	
- 모든 열(컬럼)을 가져오겠다는 뜻 (name, address, created_at 등 전체)
`FROM restaurant_restaurant`	
- 대상 테이블 이름 → restaurant_restaurant 테이블에서 가져오겠다는 뜻
`;`	
- SQL 문장의 끝 (파이썬에서는 없어도 되지만, SQL 문법상 붙이는 게 일반적)

---
테이터 확인을 위해 dbever도 실행해 줍니다.
vscode에서 dbever접속
```bash
sudo service mysql start
sudo service mysql status
```

WSL2 환경에서, IP 바뀌었다면 바뀐 ip로 서버 호스트를 변경한후 접속하세요.
![[Pasted image 20250718013905.png]]