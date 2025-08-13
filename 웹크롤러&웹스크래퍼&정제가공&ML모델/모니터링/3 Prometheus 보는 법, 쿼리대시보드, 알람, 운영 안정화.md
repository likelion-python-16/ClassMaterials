
로컬에서 FastAPI & Django 모니터링 실행 순서
FastAPI 또는 Django 서버 실행
```bash
uvicorn src.app:app --reload --port 8000
```

Django
```bash
python manage.py runserver 8900
```
FastAPI는 `localhost:8000`, Django는 `localhost:8900`에서 `/metrics` 엔드포인트가 열려 있어야 함.

fast api 또는 장고 아무데서나 실행하면 됩니다:
Prometheus 실행 (Docker)
```bash
docker run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

Grafana 실행 (Docker)
```bash
docker run -d --name=grafana \
  -p 3000:3000 \
  grafana/grafana
```

먼저 Prometheus에서 확인
1. 브라우저 열고 → **[http://localhost:9090/targets](http://localhost:9090/targets)**
2. `fastapi` 타겟이 UP 인지 확인
3. 브라우저에서 → **[http://localhost:9090/graph](http://localhost:9090/graph)**
    - Query 입력: `up{job="fastapi"}`
    - Execute 클릭 → 값이 `1`이면 서버 살아있음

데이터가 진짜 보이는지 테스트
(A) 트래픽 조금 발생시키기 : 터미널에서 실행
```bash
# FastAPI 루트(또는 임의 엔드포인트) 30번 호출
for i in {1..30}; do curl -s -o /dev/null http://localhost:8000/; done

# Django(admin 로그인 페이지 등) 10번 호출
for i in {1..10}; do curl -s -o /dev/null http://localhost:8900/admin/login/; done
```

(B) Grafana에서 조회 : Grafana에서 실행
- 좌측 Explore → Data source: `prometheus`
- 쿼리 입력 후 Run query:
1. 서버 살아있나
```
up
```

2. FastAPI RPS(초당 요청 수)
```
sum(rate(fastapi_request_count_total[1m]))
```

3. FastAPI P95 지연(최근 5분)
```
histogram_quantile(
  0.95,
  sum(rate(fastapi_request_latency_seconds_bucket[5m])) by (le)
)
```

4. Django RPS
```
histogram_quantile(
  0.95,
  sum(rate(django_http_request_duration_seconds_bucket[5m])) by (le)
)
```
그래프/테이블에 값이 보이면 연결 끝!

---
대시보드 3종(가장 기본)
1. Health (up) : 살아있는지 여부    
2. RPS : 초당 요청 수
3. P95 Latency : 95% 요청이 이 시간보다 빨리 응답함

작업 순서 (서버가 접속된 상태에서)
1. Grafana 접속 → `http://localhost:3000`
2. 왼쪽 메뉴 → “+ Create” → Dashboard
3. Add a new panel
4. Query에 위 표의 쿼리 중 하나 입력  
    (Prometheus 데이터 소스 선택)
5. 시각화 형태 선택(Stat, Time series)
6. Save & Apply
이걸 Health, RPS, P95로 각각 3번 하면 끝.

초보자 필수 Grafana 쿼리 3종
![[Pasted image 20250813173754.png]]

RPS
- FastAPI: `sum(rate(fastapi_request_count_total[1m]))`  
- Django: `sum(rate(django_http_requests_total_by_method_total[1m]))`

P95 지연
- FastAPI:  
	`histogram_quantile(0.95, sum(rate(fastapi_request_latency_seconds_bucket[5m])) by (le))`  
- Django:  
	`histogram_quantile(0.95, sum(rate(django_http_request_duration_seconds_bucket[5m])) by (le))`

필수 PromQL 개념
![[Pasted image 20250813172015.png]]

**Metric 선택**
- 수집된 데이터의 이름을 그대로 입력 → CPU 사용률 데이터를 가져옴
```
node_cpu_utilization
```

**Label 필터링** (`{}` 안에서 조건)
- 특정 서버, 경로, 상태코드 등만 골라서 조회 → `host1` 서버의 CPU만 조회
```
node_cpu_utilization{instance="host1"}
```

**함수 사용**
- `rate()` : 초당 변화량
- `sum()` : 합계
- `histogram_quantile()` : P95, P99 같은 퍼센타일 계산 → 최근 10분간 초당 요청 수
```
rate(http_requests_total[10m])
```

![[Pasted image 20250813172021.png]]

1) 바로 써먹는 쿼리 (Prometheus → Graph 탭)
- 살아있는지:  
    `up`  
    (값이 1이면 OK)
![[Pasted image 20250813153119.png]]

필수 모니터링 항목 (FastAPI / Django 공통)
![[Pasted image 20250813153821.png]]

📋 모니터링 3단계
1. 살아있나? → `up`  
    (0이면 서버 죽음 → 서버 재시작 or 장애 대응)
2. 정상 응답하나? → 요청 수 대비 500 에러 비율 확인
```
rate(fastapi_request_count_total{status_code="500"}[5m])
```
5분 동안 초당 에러 건수 확인

3. 느려지진 않나? → 응답 P95/P99
```
histogram_quantile(
  0.95,
  sum(rate(fastapi_request_latency_seconds_bucket[5m])) by (le)
)
```
(Django면 `django_http_request_duration_seconds_bucket`로 교체)

---
포트폴리오에 넣을 “딱 핵심” 구성

1. 대시보드 3종 (이미 세팅한 흐름 그대로)
- Health: `up{job=~"fastapi|django"}`
- RPS:
    - FastAPI: `sum(rate(fastapi_request_count_total[1m]))`
    - Django: `sum(rate(django_http_requests_total_by_method_total[1m]))`
- P95 Latency:
    - FastAPI: `histogram_quantile(0.95, sum(rate(fastapi_request_latency_seconds_bucket[5m])) by (le))`
    - Django: `histogram_quantile(0.95, sum(rate(django_http_request_duration_seconds_bucket[5m])) by (le))`
    
2. **오류율 패널(선택)**
```
sum(rate(fastapi_request_count_total{status_code=~"5.."}[5m]))  / sum(rate(fastapi_request_count_total[5m]))
```
(단위: Percent)

3. **부하 스크립트(데모)**
```
# FastAPI 엔드포인트 200회 for i in {1..200}; do curl -s -o /dev/null http://localhost:8000/; done
```
→ 그래프가 즉시 변하는 걸 시연.

---
제출물(Deliverables) 체크리스트
- `README.md`에 **Monitoring** 섹션 추가
    - 구성도(“FastAPI/Django → /metrics → Prometheus → Grafana”) 한 장
    - 실행 방법(아래 docker-compose 예)과 접속 URL
    - 대시보드 스크린샷 2~3장(평시, 부하시, 에러시)
        
- `docker-compose.yml` (원클릭 실행)
- `prometheus.yml`
- Grafana **Dashboard JSON**(Export해서 `grafana/` 폴더에 포함)
- 간단 **부하 스크립트**(`scripts/warmup.sh`)

---
README에 넣을 소개 문구(짧게)
- “서비스 상태(UP), 초당 요청 수(RPS), P95 응답지연을 실시간 모니터링”
- “부하 스크립트로 트래픽 발생 → 대시보드에서 변화 확인”
- “배포 전후 지연시간 비교로 최적화 효과 검증”
    
---
면접에서 이렇게 말하기
- “문제를 숫자로 본다: **UP/RPS/P95**를 항상 확인”
- “이상 징후(에러율·지연 급등) 발생 시 **원인 가설** 세우고 로그/쿼리로 추적”
- “튜닝 전/후 **그래프 비교**로 개선 증빙”

---
주의 & 팁
- 개인 정보/비밀 키가 **메트릭/스크린샷**에 노출되지 않게
- 대시보드 JSON은 “데모용”으로 간단히, 복잡한 알람은 생략해도 충분
- 실행 가이드엔 **3줄 요약** 제공:
    1. `docker compose up -d`
    2. FastAPI: [http://localhost:8000](http://localhost:8000), Django: [http://localhost:8900](http://localhost:8900)
    3. Prometheus: :9090, Grafana: :3000 (admin / admin)

---
###### 서버/시스템 지표
| 지표 종류               | 설명                          | 활용 예시                               |
| ------------------- | --------------------------- | ----------------------------------- |
| CPU 사용률             | CPU 코어들이 얼마나 바쁘게 일하고 있는지(%) | 90% 이상 계속 유지되면 CPU 증설·최적화 필요        |
| 메모리 사용량             | RAM의 현재 사용량 및 남은 용량         | 메모리 누수 여부 확인, OOM(Out Of Memory) 방지 |
| 디스크 사용량             | SSD/HDD의 사용량 및 남은 공간        | 로그, 데이터베이스 용량 관리                    |
| 디스크 I/O             | 초당 읽기/쓰기 속도                 | DB나 파일 서버 병목 원인 분석                  |
| 네트워크 트래픽            | 초당 송수신 데이터량                 | 트래픽 급증 시 DDoS 탐지, 네트워크 용량 확장        |
| 프로세스 수              | 서버에서 실행 중인 프로세스 개수          | 비정상적인 프로세스 폭증 탐지                    |
| 로드 평균(Load Average) | CPU가 동시에 처리하려는 작업 큐 길이      | 서버 과부하 여부 판단                        |

어디에 사용되나?
1. 장애 예방 (Preventive Monitoring)
    - 예: 디스크 사용률이 90%를 넘기면 경고 알림 발송 → 서비스 중단 전 조치 가능
    - CPU 부하 급증 감지 후 트래픽 우회나 스케일 아웃(서버 증설) 결정
        
2. 성능 최적화 (Performance Tuning)
    - 서버 리소스가 어떤 시간대에 가장 많이 쓰이는지 분석 → 부하 분산 스케줄링
    - 예: 매일 오후 2시 CPU 90% → 배치 작업 시간 변경
        
3. 장애 원인 분석 (Troubleshooting)
    - "왜 서버가 느려졌나?" → CPU, 메모리, 디스크, 네트워크 사용량 변화 추적
    - 예: 네트워크 트래픽 급증 → 특정 API 요청 폭발
        
4. 용량 계획 (Capacity Planning)
    - 데이터 증가 속도와 디스크 사용량 추세를 분석 → 서버 증설 시기 예측
    - 예: 현재 속도면 3개월 후 디스크 꽉 참 → 미리 스토리지 추가

---
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