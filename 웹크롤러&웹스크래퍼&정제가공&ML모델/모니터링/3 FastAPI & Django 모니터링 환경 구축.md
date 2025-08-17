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

Grafana 볼륨생성(1회만) : 터미널에서
```bash
docker run -d --name grafana -p 3000:3000 \
  --add-host=host.docker.internal:host-gateway \
  -v grafana-data:/var/lib/grafana \
  grafana/grafana
```

- 접속: [http://localhost:3000](http://localhost:3000)
- 로그인: `admin / admin` (처음에 비밀번호 변경)

Grafana를 처음 설치하고 로그인했을 때 나오는 기본 홈 화면
![[Pasted image 20250813155751.png]]

![[Pasted image 20250813160909.png]]

![[Pasted image 20250813160916.png]]

Explore data 버튼클릭후 Prometheus에서 수집한 데이터를 바로 조회해볼 수 있습니다.
![[Pasted image 20250813162457.png]]
`http://host.docker.internal:9090`

![[Pasted image 20250813160931.png]]

Grafana → Data sources → Prometheus 설정에서 **URL**을:
```
http://host.docker.internal:9090
```
Save & test → Success 떠야 정상

데이터 소스 타입이 아직 선택되지 않은 상태로 상단탭에 Data sources 클릭
![[Pasted image 20250813162057.png]]

그라파나 실행하기
![[Pasted image 20250817221445.png]]

서버가 살아있나 테스트하기
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
프로메테우스 켜는 방법 정리

(한 번만) 최초 설정
```bash
# 1) 공용 네트워크
docker network create observability || true

# 2) Grafana 데이터/프로비저닝
mkdir -p ~/AIRestaurant/grafana/data
mkdir -p ~/AIRestaurant/grafana/provisioning/datasources
cat > ~/AIRestaurant/grafana/provisioning/datasources/prometheus.yml <<'EOF'
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

# 3) Prometheus 컨테이너(설정파일 폴더에서 실행)
cd ~/AIRestaurant/prometheus-2.54.1.linux-amd64
docker run -d --name prometheus \
  --restart unless-stopped \
  --network observability \
  --add-host=host.docker.internal:host-gateway \
  -p 9090:9090 \
  -v "$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus

# 4) Grafana 컨테이너
docker run -d --name grafana \
  --restart unless-stopped \
  --network observability \
  -p 3000:3000 \
  -v ~/AIRestaurant/grafana/data:/var/lib/grafana \
  -v ~/AIRestaurant/grafana/provisioning:/etc/grafana/provisioning \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana

# 5) node_exporter 컨테이너
docker run -d --name node_exporter \
  --restart unless-stopped \
  --network observability \
  -p 9100:9100 \
  prom/node-exporter
```

(매일) 실행순서
로컬에서 FastAPI & Django 모니터링 실행 순서
FastAPI 또는 Django 서버 실행
```bash
source ~/fastdining_api/.venv/bin/activate
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```
- `--host` → IP 주소나 호스트 지정 (`0.0.0.0`은 외부 접속 허용 의미)
- `--port` → 숫자만 입력 (예: `8000`)

Django
```bash
source ~/AIRestaurant/.venv/bin/activate
python manage.py runserver 0.0.0.0:8900
```
FastAPI는 `localhost:8000`, Django는 `localhost:8900`에서 `/metrics` 엔드포인트가 열려 있어야 함.

Prometheus & Grafana (기존 컨테이너 재사용)
```bash
docker start prometheus grafana node_exporter
```

- Prometheus Targets: [http://localhost:9090/targets](http://localhost:9090/targets) → **fastapi/django/node_exporter = UP**
- Grafana: [http://localhost:3000](http://localhost:3000) (admin / admin)

Grafana도 그 안에서 같이 관리되므로, 따로 `docker run`으로 띄울 필요가 없습니다
매번 `docker run …` 으로 띄우면 실행할 때마다 옵션/볼륨/네트워크를 수동으로 넣어줘야 해서 불편함을 고정방식으로 작성하는 방법
`docker-compose.yml` 작성
```yml
version: "3.9"

networks:
  observability:
    driver: bridge

services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    restart: unless-stopped
    networks:
      - observability
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus-2.54.1.linux-amd64/prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana
    container_name: grafana
    restart: unless-stopped
    networks:
      - observability
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  node_exporter:
    image: prom/node-exporter
    container_name: node_exporter
    restart: unless-stopped
    networks:
      - observability
    ports:
      - "9100:9100"
```
이렇게 하면 `docker run …` 긴 명령어를 칠 필요 없이 `compose`가 자동으로 네트워크, 볼륨, 권한까지 처리해 줍니다.

실행:
```bash
cd ~/AIRestaurant
docker compose up -d
```

종료:
```
docker compose down
```

node_exporter Docker로 설치
```bash
# node_exporter 컨테이너 실행
docker run -d --name=node_exporter \
  -p 9100:9100 \
  --restart=unless-stopped \
  prom/node-exporter
```

경로를 꼭 확인하세요. 
`/home/youjung/fastdining_api/prometheus-2.54.1.linux-amd64/prometheus.yml`

`/home/youjung/AIRestaurant/prometheus-2.54.1.linux-amd64/prometheus.yml`

Django와 fast api `prometheus.yml`파일에 각각 추가
```yml
# ===========================
# Prometheus 기본 전역 설정
# ===========================
global:
  scrape_interval: 15s  #기본 수집 주기 (15초마다 대상에서 메트릭 수집)

# ===========================
# 수집 대상(job) 목록 설정
# ===========================
scrape_configs:

  # ---------------------------
  # FastAPI 애플리케이션 메트릭
  # ---------------------------
  - job_name: "fastapi"  # 수집 대상 이름 (Prometheus에서 구분할 이름)
    metrics_path: /metrics   # FastAPI 노출하는 메트릭 엔드포인트 경로
    static_configs:
      - targets: ["localhost:8000"]  # 메트릭 서버 주소 (포트 8000)

  # ---------------------------
  # Django 애플리케이션 메트릭
  # ---------------------------
  - job_name: "django"
    metrics_path: /metrics
    static_configs:
      - targets: ["localhost:8900"]  # Django 서버 주소 (포트 8900)

  # ---------------------------
  # Node Exporter (서버 리소스 모니터링)
  # ---------------------------
  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]  
      # Node Exporter 실행 포트 (서버 CPU, 메모리 등)

  # ---------------------------
  # Prometheus 자기 자신 모니터링
  # ---------------------------
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]  # Prometheus 서버 자체 메트릭
```

/익스포터가 실제로 떠있는지 (호스트에서 확인)
```bash
curl -sI http://localhost:8000/metrics | head -n1   # FastAPI
curl -sI http://localhost:8900/metrics | head -n1   # Django
curl -sI http://localhost:9100/metrics | head -n1   
# node_exporter (띄웠다면)
```
모두 `HTTP/1.1 200 OK`면 OK (FastAPI는 GET으로만 확인해도 괜찮음).


```bash
# 1) 기존 컨테이너 제거
docker rm -f prometheus 2>/dev/null || true

# 2) 재실행 (핵심: --add-host=host.docker.internal:host-gateway)
docker run -d --name prometheus \
  -p 9090:9090 \
  --add-host=host.docker.internal:host-gateway \
  -v "$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  prom/prometheus
```