공식문서 링크[https://fastapi.tiangolo.com/ko/](https://fastapi.tiangolo.com/ko/)

FastAPI는 **Python**으로 만든 빠르고 현대적인 웹 프레임워크입니다. 주로 REST API 서버를 구축할 때 사용되며, 이름 그대로 매우 빠른 속도와 생산성을 자랑합니다.

FastAPI란?
> FastAPI = Python + Starlette(비동기 웹서버) + Pydantic(데이터 검증)  
> → 빠르고, 자동화된 문서 제공, 타입 기반 코드 작성이 가능한 API 서버 프레임워크

###### 주요 특징
| 특징           | 설명                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| 빠른 성능        | 웹 요청을 빠르게 처리할 수 있어, Node.js나 Go처럼 빠른 웹 서버제작가능, 내부적으로는 Starlette라는 빠른 엔진을 사용하고, 비동기 방식으로 동시에 여러 작업을 처리가능 |
| 자동 데이터 검증    | `Pydantic`을 통해 입력값 자동 검증 (ex: 나이는 int여야 한다 등)                                                           |
| 자동 API 문서 생성 | `/docs` (Swagger), `/redoc` 경로로 API 문서 자동 생성                                                            |
| 타입 힌트 기반 코드  | Python의 타입 힌트를 적극 활용하여 자동 검증 및 IDE 지원 향상                                                                |
| 비동기 지원       | `async/await` 사용하여 높은 처리량 확보 가능                                                                         |
| 간단한 구조       | Django보다 훨씬 가볍고 직관적인 API 설계                                                                             |

FastAPI는 언제 사용할까?
- 백엔드 API 서버 만들 때 (React/Vue와 연결)
- AI/머신러닝 모델 API 서버 (모델 서빙)
- 간단한 백엔드 서비스 개발 (CRUD, 인증, DB 처리)
- 비동기/고성능 서버 구축할 때

###### Django vs FastAPI
| 항목     | Django       | FastAPI         |
| ------ | ------------ | --------------- |
| 목적     | 풀스택 웹 프레임워크  | API 전용 백엔드      |
| 비동기    | 제한적 지원       | 완전 지원           |
| 속도     | 보통           | 빠름              |
| 문서 자동화 | X (추가 설정 필요) | O (기본 제공)       |
| 사용 예   | 웹사이트, 관리자페이지 | AI API, 모바일 백엔드 |

FastAPI로 할 수 있는 것들
- REST API (CRUD)
- JWT 기반 로그인 인증
- DB 연동 (SQLAlchemy, Tortoise ORM)
- 머신러닝 모델 배포
- WebSocket 실시간 통신
- 비동기 크롤러 서버

DRF의 Serializer → FastAPI의 Pydantic
- Django REST Framework에서는 데이터를 검증하거나 JSON으로 변환할 때 `Serializer`를 써요.
- FastAPI에서는 같은 역할을 `Pydantic`의 BaseModel이 해요.
```python
# DRF에서
class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()

# FastAPI에서는
class Book(BaseModel):
    title: str
    author: str
```
즉, Serializer ↔ Pydantic 모델은 1:1 대응 가능해요.

---
###### FastAPI가 Django/DRF에서 "대체 가능한 기능"
| Django/DRF 기능                    | FastAPI에서 대체 방법                   | 설명                     |
| -------------------------------- | --------------------------------- | ---------------------- |
| Serializer (`DRF`)               | `Pydantic` 모델                     | 입력값 검증, 직렬화/역직렬화 모두 처리 |
| View (`APIView`, `ViewSet`)      | 경로 함수 (`@app.get`, `@app.post` 등) | URL과 연결된 API 처리 로직 작성  |
| 권한/인증 (`IsAuthenticated`, JWT 등) | Depends + Security + OAuth2       | JWT 토큰, 인증 헤더 처리 가능    |
| URL 라우팅 (`urls.py`)              | `@app.get("/path")` 등 데코레이터 방식    | URL에 따른 함수 연결          |
| API 문서화 (`drf-yasg` 등)           | 자동 문서 생성 (`/docs`, `/redoc`)      | Swagger & ReDoc 자동 생성  |
| 테스트 (`APITestCase`, `pytest`)    | `pytest`, `httpx`, `TestClient`   | 단위 테스트 및 API 테스트 가능    |
| Request/Response 관리              | FastAPI의 `Request`, `Response` 객체 | 요청 정보 접근 및 응답 조작 가능    |

---
###### FastAPI가 Django의 기능을 **대체할 수 없는 것**
| Django 기능                     | FastAPI 대체 가능 여부 | 이유                                                               |
| ----------------------------- | ---------------- | ---------------------------------------------------------------- |
| 템플릿/HTML 렌더링                  | ❌ 일부만 가능         | Jinja2 등 외부 템플릿 사용 필요. Django처럼 완전한 HTML 렌더링 X                   |
| ORM (`models.py`, `QuerySet`) | ❌ 직접 제공 안 함      | SQLAlchemy 또는 Tortoise-ORM을 별도 사용해야 함                            |
| Admin 페이지                     | ❌ 없음             | Django의 강력한 `admin` 시스템은 FastAPI에 없음                             |
| 전체 웹서비스 구조                    | ❌                | FastAPI는 API 서버에 특화되어 있음 (회원가입/로그인/관리자 등 웹서비스 전체 구조는 Django가 강함) |

---
###### 💡 요약
| 항목                               | FastAPI로 대체 가능?         | 설명                    |
| -------------------------------- | ----------------------- | --------------------- |
| API 처리 (views, serializer, docs) | 완벽하게 가능                 | DRF를 거의 완전히 대체 가능     |
| 인증, 권한 관리                        | 일부 대체 가능                | JWT/OAuth2 등 수동 설정 필요 |
| ORM, HTML 템플릿, Admin             | Django가 강력함           . | FastAPI는 API 서버만 잘함   |

---
###### 추천 사용 예시
| 목적                          | 추천 프레임워크                                  |
| --------------------------- | ----------------------------------------- |
| CRUD API, AI 모델 서빙, 모바일 백엔드 | FastAPI                                   |
| 웹사이트, 관리자 페이지, 마케팅 페이지      | Django                                    |
| 둘 다 필요 (관리자 + API)          | Django + FastAPI 병행 (또는 Django 내부 API 개발) |



