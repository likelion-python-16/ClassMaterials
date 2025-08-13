### fast api에 프로메테우스 설치

목표
- FastAPI와 Django에 Prometheus 메트릭 엔드포인트(`/metrics`) 추가
- Prometheus 서버가 두 서비스의 메트릭을 주기적으로 수집
- Grafana로 시각화

#### 1) FastAPI: `/metrics` 추가

1. 설치
```bash
pip install prometheus-client
```

2. 코드 추가
`src/routers/metrics_router.py`에 아래 라우트 하나만 추가해도 됩니다.
```python
import time
from fastapi import APIRouter, Response, Request, FastAPI
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST
)

router = APIRouter(tags=["Monitoring"])

# ---- 메트릭 정의 ----
REQUEST_COUNT = Counter(
    "fastapi_request_count",
    "Total request count",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "fastapi_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
)
ALIVE = Gauge("fastapi_app_alive", "If app is alive: 1")
ALIVE.set(1)

# ---- /metrics 엔드포인트 ----
@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ---- 앱에 미들웨어를 붙이는 헬퍼 ----
def attach_metrics_middleware(app: FastAPI):
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        REQUEST_COUNT.labels(
            request.method, request.url.path, str(response.status_code)
        ).inc()
        REQUEST_LATENCY.labels(request.url.path).observe(duration)
        return response
```

`src/app.py`
```python
# ... (기존 import들)
from src.routers.metrics_router import router as metrics_router, attach_metrics_middleware

app = FastAPI(
    title="패스트다이닝 API",
    openapi_tags=tags_metadata
)

# 미들웨어 먼저 붙여도/나중에 붙여도 동작하지만,
# 보통 app 생성 직후 붙이는 것이 깔끔합니다.
attach_metrics_middleware(app)

# ... 기존 라우터들 include
# ...
app.include_router(metrics_router)  # /metrics 노출
```

서버 실행 (프로젝트 “루트”에서!)
```bash
# (중요) fastdining_api 루트에서 실행해야 src 패키지를 찾습니다.
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# 브라우저에서
http://localhost:8000/metrics
```

이렇게 보이면 설치 성공:
```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 517.0
python_gc_objects_collected_total{generation="1"} 76.0
python_gc_objects_collected_total{generation="2"} 16.0
..............
```

🔹 Prometheus 쪽 할 일

Fast API `prometheus.yml` 만들기
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "fastapi"
    metrics_path: /metrics
    static_configs:
      # FastAPI
      - targets: ["host.docker.internal:8000"]   

  - job_name: "django"
    metrics_path: /metrics
    static_configs:
      # Django (runserver 포트 기준)
      - targets: ["host.docker.internal:8900"] 
```

Prometheus 실행 (Docker 권장)
서버가 실행하고 있을때 bash를 추가하여 터미널에서 입력합니다.
```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

---
### Django `/metrics` 추가

패키지 설치
```bash
pip install django-prometheus
```

`settings.py` 설정 INSTALLED_APPS
```python
INSTALLED_APPS = ["django_prometheus", ...]
MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    ...,
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
```


DB 엔진 래퍼 적용
```python
DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "restaurant_db"),
        "USER": os.environ.get("DB_USER", "django_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "db_password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {"charset": "utf8mb4"},
    },
        "fdc": {     
        "ENGINE": "django_prometheus.db.backends.mysql",
        "NAME": "myproject_db",
        "USER": "django_user",
        "PASSWORD": "DjangoUserPass!123",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    },
}
```

`urls.py`에 /metrics 등록
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # ✅ /metrics 엔드포인트 추가
    path("", include("django_prometheus.urls")), 
    path("", include("restaurant.urls")),
]
```

Django `prometheus.yml`
```yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "fastapi"
    metrics_path: /metrics
    static_configs:
      # FastAPI
      - targets: ["host.docker.internal:8000"]   

  - job_name: "django"
    metrics_path: /metrics
    static_configs:
      # Django (runserver 포트 기준)
      - targets: ["host.docker.internal:8900"]   
```

Docker로 실행
```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

브라우저 `http://localhost:9090` → Status > Targets에서  
`fastapi`, `django` 두 job이 UP이면 정상입니다.
```
http://localhost:9090/targets
```

FastAPI
```
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

Django
```
python manage.py runserver 0.0.0.0:8900
```

설치 성공
![[Pasted image 20250813151017.png]]

----
### Grafana로 시각화

Grafana 띄우기
```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```
- 접속: [http://localhost:3000](http://localhost:3000)
- 로그인: `admin / admin` (처음에 비밀번호 변경)

Grafana를 처음 설치하고 로그인했을 때 나오는 기본 홈 화면
![[Pasted image 20250813155751.png]]

![[Pasted image 20250813160909.png]]

![[Pasted image 20250813160916.png]]

![[Pasted image 20250813160923.png]]

![[Pasted image 20250813160931.png]]

혹시 이런 에러가 뜬다면:
![[Pasted image 20250813161103.png]]그 에러는 Grafana가 도커 컨테이너로 떠 있고, Prometheus는 WSL(호스트) 9090에서 돌기 때문이에요.  
컨테이너 입장에서 `localhost:9090`은 자기 자신이라서 접속이 거부됩니다.

컨테이너에서 호스트로 붙기
Grafana 컨테이너 재생성(호스트 매핑 추가)
```bash
docker rm -f grafana
docker run -d --name grafana \
  -p 3000:3000 \
  --add-host=host.docker.internal:host-gateway \
  grafana/grafana
```

Grafana → Data sources → Prometheus 설정에서 **URL**을:
```
http://host.docker.internal:9090
```
Save & test → Success 떠야 정상

데이터 소스 타입이 아직 선택되지 않은 상태로 상단탭에 Data sources 클릭
![[Pasted image 20250813162057.png]]

Explore data 버튼클릭후 Prometheus에서 수집한 데이터를 바로 조회해볼 수 있습니다.
![[Pasted image 20250813162457.png]]

![[Pasted image 20250813162638.png]]
- Metric 드롭다운 클릭 → 리스트에서 `up` 선택
    - `up` 메트릭은 Prometheus가 모니터링 중인 타겟이 살아있는지(1) 죽었는지(0) 알려주는 기본 테스트 메트릭이에요.
- 우측 상단의 Run query 버튼 클릭
- 아래 그래프/테이블에 데이터가 뜨는지 확인
![[Pasted image 20250813163032.png]]

정리하면:
- Prometheus → 데이터를 수집하는 도구 (CPU 사용량, 메모리, API 응답 속도 등)
- Grafana → 그 데이터를 예쁘게 시각화하고 대시보드로 보여주는 도구

---
