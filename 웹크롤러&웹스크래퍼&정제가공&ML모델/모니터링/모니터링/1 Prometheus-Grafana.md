#### 1) 모니터링이란? (What & Why)

모니터링(Monitoring) 은  
👉 서비스가 잘 작동하고 있는지 숫자와 그래프로 확인하는 활동입니다.

왜 필요할까요?
- 서비스가 살아있는지 확인 (가용성)  
    서버가 죽었는데 모르고 있으면 곤란하죠.
    
- 속도가 충분히 빠른지 확인 (성능)  
    평균 응답속도뿐 아니라 “95%의 요청은 0.3초 안에 끝났는지?” 같은 p95/p99 지표를 봅니다.
    
- 에러가 얼마나 나는지 확인 (안정성)  
    에러율이 1%인지, 0.01%인지에 따라 사용자 경험이 달라져요.
    
- 서버 자원 상태 확인 (병목)  
    CPU/메모리/디스크가 꽉 차면 서비스가 느려지거나 멈춥니다.
    
- AI가 붙은 경우라면  
    모델 호출이 느린지, 실패율이 높은지, API 비용이 많이 나가는지 → 전부 숫자로 확인할 수 있어야 합니다.
    
즉, 모니터링은 “서비스 건강검진” 같은 거예요

---
#### 2) 모니터링할 대상 (What)

![[Pasted image 20250813131454.png]]

Prometheus에서 모니터링하는 기본 단위는 Metric(메트릭) 입니다.  
메트릭은 4가지 타입이 있어요:

1. Counter (누적되는 값)
    - 예: `http_requests_total` (지금까지 받은 HTTP 요청 수)
    - 계속 증가만 함 (초기화는 서버 재시작 시)
        
2. Gauge (현재값)
    - 예: `node_memory_usage_bytes` (현재 메모리 사용량)
    - 늘었다 줄었다 가능
        
3. Histogram (분포 + 버킷)
    - 예: `http_request_duration_seconds_bucket`
    - 요청 시간을 “0.1초 이하 / 0.5초 이하 / 1초 이하 …” 로 나눠 카운트
    - 여기서 p95/p99 같은 백분위수를 계산할 수 있음
        
4. Summary (요약)
    - 비슷하게 백분위수를 제공하지만, 보통은 Histogram을 더 많이 씀.
        
![[Pasted image 20250818085034.png]]

그리고 라벨(Label)을 붙여서 더 세밀하게 구분합니다.  
예시:
```
http_requests_total{method="GET", endpoint="/login", status="200"} 
http_requests_total{method="POST", endpoint="/ai", status="500"}
```

👉 이렇게 하면 "로그인 성공 횟수" vs "AI 호출 실패 횟수"를 따로 볼 수 있어요. 
다만 이런 라벨은 기본으로 붙는 게 아니고, Counter/Gauge/Histogram을 정의할 때 라벨을 추가해주는 코드(또는 자동 계측 라이브러리 설정)가 필요합니다.

---
#### 3) 동작 흐름 (How)

모니터링 시스템은 **3단계**로 동작합니다.

1. App이 /metrics 노출
    - Django, FastAPI 같은 서버에 `prometheus_client` 라이브러리를 설치하면  `/metrics` URL에서 메트릭이 노출됩니다.
    - 이 URL을 브라우저에서 열어보면 텍스트 형식의 숫자들이 쭉 나옵니다.
```python
# FastAPI 예시 (src/app.py)
from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()
REQUESTS = Counter("http_requests_total", "총 요청 수")

@app.get("/")
def hello():
    REQUESTS.inc()   # 카운터 +1
    return {"msg": "hello"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
```
    👉 이 코드는 FastAPI 서버 파일 (예: src/app.py) 에 넣습니다.
    
2. Prometheus가 긁어감 (Scraping)
    - Prometheus 서버가 15초마다 `http://localhost:8000/metrics` 같은 경로를 호출해서 데이터를 가져옵니다.
    - 이 경로는 `prometheus.yml` 설정 파일에 적습니다.
        
```yml
scrape_configs:
  - job_name: "fastapi"
    metrics_path: /metrics
    static_configs:
      - targets: ["localhost:8000"]
```
    
3. **Grafana로 시각화 & 알림**
    - Prometheus가 모은 데이터를 Grafana에서 쿼리하면  
        시간에 따른 그래프, 대시보드, 알림(슬랙/이메일)까지 설정할 수 있습니다.
    - 예: `rate(http_requests_total[5m])` → 최근 5분간 초당 요청 수
        
---
#### 4) 초보 개발자가 알아야 할 것

처음 배울 때는 **이 네 가지 키워드만 확실히** 이해하면 돼요.
- **Counter / Gauge / Histogram / Label** → 메트릭의 기본 단위
- **/metrics 엔드포인트** → 앱이 노출하는 지표
- **Prometheus** → 지표 저장 (DB 역할)
- **Grafana** → 지표 시각화 & 알림
    
---
✅ **정리**

- **왜?** 서비스 상태(가용성·성능·안정성·자원·AI비용)를 숫자로 보려고.
- **무엇?** Counter, Gauge, Histogram, Label 로 세분화된 메트릭.
- **어떻게?**
    1. 앱에서 `/metrics` 열기 →
    2. Prometheus가 긁어서 저장 →
    3. Grafana에서 시각화 & 알림.

시계열 데이터 : 
![[Pasted image 20250813114936.png]]