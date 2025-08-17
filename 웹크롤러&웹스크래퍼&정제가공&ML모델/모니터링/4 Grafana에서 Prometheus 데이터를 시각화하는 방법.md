
![[Pasted image 20250817122837.png]]

![[Pasted image 20250817123642.png]]

데이터가 진짜 보이는지 테스트
(A) 트래픽 조금 발생시키기 : 터미널에서 실행
```bash
# FastAPI 루트(또는 임의 엔드포인트) 30번 호출
for i in {1..30}; do curl -s -o /dev/null http://localhost:8000/; done

# Django(admin 로그인 페이지 등) 10번 호출
for i in {1..10}; do curl -s -o /dev/null http://localhost:8900/admin/login/; done
```
- 윈도우 조정: `[1m]`(민감) ↔ `[5m]`(적당) ↔ `[10m]`(부드러움)
- /metrics 제외: `{endpoint!="/metrics"}`를 습관처럼 사용
---
자주 쓰는 표기들
- RPS = Requests Per Second (초당 요청 수)
- RPM = Requests Per Minute (분당 요청 수)
- QPS = Queries Per Second (주로 DB/검색 쿼리)
- TPS = Transactions Per Second (트랜잭션)
---
1. 총 RPS(초당 요청 수) 값이 올라가면 ‘요청 수(트래픽)’가 증가했다는 뜻입니다.
```
sum(rate(fastapi_request_count_total{endpoint!="/metrics"}[5m]))
```

![[Pasted image 20250817191126.png]]
“최근 5분 동안 평균적으로 초당 몇 건 처리했나” 를 뜻해요
그래프 해석 (화면 기준)
- 왼쪽 구간의 0.88~0.9: 최근 5분 창에서 평균 약 0.9 req/s 처리.  
    → 분당으로는 0.9 × 60 = 약 54 req/min.(`req`는 request(리퀘스트, “요청”)의 줄임말이에요.)
- 19:00 근처에 계단형 하락 → 0: 트래픽을 멈추자, 5분 이동창에서 과거 요청이 점점 빠져나가며 값이 0으로 감쇠.
- 19:09~19:13에 0.35~0.4 부근: 그 구간엔 평균 약 0.35~0.4 req/s(분당 21~24건) 정도 트래픽이 있었다는 뜻.
- 다시 0으로 하락: 그 뒤 5분 창에 남은 요청이 없어지면서 0으로 떨어짐.
    
> 포인트: `rate(...[5m])`는 이 시각 기준 직전 5분을 봅니다(슬라이딩 창).  
> 그래서 트래픽을 갑자기 멈춰도 즉시 0이 아니라 “서서히” 0으로 내려와요.
---

0.4 req/s는  
→ “초당 0.4건의 요청” = 0.4 requests per second 라고 읽습니다.  
대충 분당으로는 `0.4 × 60 = 약 24건/min`이에요.

---
2. 메서드/상태별 RPS
```
sum by (method, status_code)(
  rate(fastapi_request_count_total{endpoint!="/metrics"}[5m])
)
```

![[Pasted image 20250817192450.png]]
이 쿼리가 뜻하는 것
- **`fastapi_request_count_total`**: 요청 “누적(카운터)” 메트릭.
- **`rate(...[5m])`**: “최근 5분 동안 초당 몇 건 증가했는가” → RPS(requests/sec).
- **`sum by (method, status_code)`**: 나머지 라벨(예: endpoint, instance)을 합계하고,  `method`·`status_code` 조합별로 한 줄씩 보여줍니다.
- **`{endpoint!="/metrics"}`**: Prometheus가 긁는 `/metrics` 호출은 제외.
    
그래프를 읽는 방법 (화면 기준)
- Y축: RPS(초당 요청 수). `0.35`라면 0.35 req/s ≈ 분당 21건.
- 범례: `(method="GET", status_code="200")` → “성공한 GET 요청” 라인 하나를 보고 있다는 뜻.
- 왼쪽의 0.88 근처 평지: 최근 5분 창 평균으로 **약 0.88 req/s** 처리.
- 19:00 근처의 계단형 하락 → 0: 트래픽을 멈추자, 5분 이동창에서 과거 샘플이 빠지며 값이 서서히 0으로.
- 19:09~19:13의 0.35 안팎 평지: 그때는 평균 **0.35 req/s** 정도의 트래픽이 있었다는 뜻.
- 다시 0: 최근 5분에 해당 요청이 없다는 뜻.
    
> 포인트: `rate([5m])`는 “지금 시각 기준 직전 5분”을 보는 이동창이라 갑자기 멈춰도 값이 부드럽게 감쇠합니다.

이 패널로 알 수 있는 것 / 알 수 없는 것
- 알 수 있음: “성공한 GET 요청이 시간대별로 얼마나 들어왔나(RPS 추이)”
- 알 수 없음: 지연시간, 에러율. → 별도 패널로 봐야 함.

---
3. p95 지연시간(초)
```
histogram_quantile(
  0.95,
  sum by (le) (rate(fastapi_request_latency_seconds_bucket[5m]))
)
```

![[Pasted image 20250817193128.png]]
- **`fastapi_request_latency_seconds_bucket`**: 응답 지연시간 히스토그램 버킷(초).
- **`rate(...[5m])`**: 최근 **5분** 동안 버킷별 증가량/초(슬라이딩 윈도우).
- **`sum by (le)`**: 모든 라벨(엔드포인트/메서드/인스턴스 등)을 합쳐서 버킷 경계(`le`)만 남김 → “서비스 전체 분포”.
- **`histogram_quantile(0.95, …)`**: 그 분포에서 p95(95번째 퍼센타일) 추정

그래프를 읽는 방법 (화면 기준)
- Y축 단위: 초(s).  
    그래프가 0.27에 있으면 “최근 5분 동안의 요청 중 95%가 **0.27초(=270ms)** 이내에 끝났다”는 뜻이에요.
- 스크린샷처럼 잠깐 솟은 봉우리는 그 시점에 느린 요청(예: `/slow`)이 섞여 tail이 늘었다는 신호.
    
- 값이 0 근처로 평평하면:
    - 최근 5분 동안 요청이 거의 없거나(rate가 0),
    - 모두 매우 빨랐거나,
    - 테스트를 `/metrics`만 때린 경우일 수 있어요.

단위를 ms로: 식 끝에 `* 1000` 붙이고 Panel Unit을 `milliseconds`로.
```
1000 *
histogram_quantile(0.95, sum by (le) (rate(fastapi_request_latency_seconds_bucket[5m])))
```

엔드포인트별 p95:
```
histogram_quantile(
  0.95,
  sum by (le, endpoint) (
    rate(fastapi_request_latency_seconds_bucket{endpoint!="/metrics"}[5m])
  )
)
```
- → 느린 라인이 어느 경로인지 바로 보입니다.
- p50 / p99도 동일: `0.50`, `0.99`로 바꾸기만 하면 돼요.
- SLO 선 그리기: Panel → Thresholds에 예) 800ms(0.8s) 추가.

---
4. 5xx 에러율(%) 
```
100 *
( sum(rate(fastapi_request_count_total{endpoint!="/metrics", status_code=~"5.."}[5m])) or vector(0) )
/
clamp_min(
  sum(rate(fastapi_request_count_total{endpoint!="/metrics"}[5m])),
  1
)
```

![[Pasted image 20250817194132.png]]
- 최근 5분 동안의 전체 요청(RPS) 대비 5xx 요청(RPS) 의 백분율입니다.
- 그래프가 0% 근처에 붙어있다 → 최근 5분 동안 5xx가 없었거나 매우 드물었다는 뜻.
- 
쿼리 각 부분 뜻
- `rate(...[5m])` : 직전 5분 창에서 초당 증가량(=RPS).
- `status_code=~"5.."` : 500–599 서버 오류만 집계.
- `endpoint!="/metrics"` : Prometheus의 스크랩 요청은 제외.
- `sum(...)` : 인스턴스/엔드포인트 등 라벨을 모두 합계.
- `or vector(0)` : 5xx가 전혀 없을 때도 값이 빈 벡터가 아니라 0이 되도록.
- `clamp_min(..., 1)` : 분모(RPS 합계)가 0일 때 0으로 나누기 방지(에러율을 0%로 처리).
- 맨 앞의 `100 *` : 비율 → 퍼센트(%) 로 변환.

그래프를 읽는 방법 (화면 기준)
- Y축 단위: `%` 로 설정하는 게 좋습니다(Panel → Unit → _percent (0–100)_).
- 값이 0%에 붙어 있으면:
    - (a) 최근 5분 동안 5xx가 없음, 또는
    - (b) 최근 5분 동안 전체 RPS가 0 (트래픽 없음) — 이 경우에도 위 쿼리는 0%로 보여줍니다.
- 스파이크가 2%처럼 보이면: “해당 시점의 최근 5분 창에서 전체 요청 100건 중 2건이 5xx였다”는 감각입니다. 윈도우가 이동하므로 시간이 지나면 자연히 내려갑니다.

테스트/디버깅 팁
- 일부러 5xx 내보기(있다면 `/boom` 엔드포인트):
```bash
for i in {1..5}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/boom; done
```
→ 잠깐 에러율이 >0%로 튀는지 확인.

분자/분모를 따로 보며 검증:
```
sum(rate(fastapi_request_count_total{endpoint!="/metrics", status_code=~"5.."}[5m])) 
# 분자(5xx RPS)

sum(rate(fastapi_request_count_total{endpoint!="/metrics"}[5m]))  
# 분모(전체 RPS)
```
응용(원인 빠르게 찾기)
- 엔드포인트별 5xx 비율:
```
100 *
sum by (endpoint)(rate(fastapi_request_count_total{endpoint!="/metrics", status_code=~"5.."}[5m]))
/
clamp_min(sum by (endpoint)(rate(fastapi_request_count_total{endpoint!="/metrics"}[5m])), 1)
```
메서드/상태별 5xx RPS(절대값):
```
sum by (method, status_code)(
  rate(fastapi_request_count_total{endpoint!="/metrics", status_code=~"5.."}[5m])
)
```

---
대시보드 3종(가장 기본)
1. Health (up) : 살아있는지 여부    
2. RPS : 초당 요청 수
3. P95 Latency : 95% 요청이 이 시간보다 빨리 응답함

초보자 필수 Grafana 쿼리 3종
![[Pasted image 20250813173754.png]]

필수 PromQL 개념
![[Pasted image 20250813172015.png]]

인스턴스(호스트)별 CPU 사용률(%)
```
100 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100
```

![[Pasted image 20250817195926.png]]
- `node_cpu_seconds_total{mode="idle"}`: CPU가 **idle** 상태였던 누적시간.
- `rate(...[5m])`: **최근 5분** 동안 idle의 **비율(0~1)**.
- `avg by (instance)`: 코어별 값을 **호스트 단위 평균**으로 합침.
- `100 - (...) * 100`: idle%를 뒤집어 **사용률 %**로 변환.
    
즉, “최근 5분 이동창 기준, 호스트별 CPU 사용률(%)”을 그립니다.

그래프를 읽는 방법 (화면 기준)
- Y축 값은 “CPU 사용률 %”. 예: 5면 5% 사용, 55면 55% 사용.
- 왼쪽의 약 55% → 급감 → 수 분간 3~5% → 다시 상승:
    - 그 구간에서 한동안 부하가 컸다가(55%),  
        요청/작업이 줄어들며 거의 유휴 상태(3~5%)가 되었고,  
        이후 다시 부하가 생김을 의미합니다.
- 계단처럼 부드럽게 변하는 이유: 5분 이동창`(rate[5m])`이라 과거 샘플이 점점 빠져나가며 완만히 변합니다.

패널 설정
![[Pasted image 20250817201650.png]]
 `1)` Title 바꾸기
- 우측 사이드바 상단 **Panel options** 섹션 → **Title** 입력란에  
    `CPU usage % (5m avg)` 처럼 적기 → 위쪽 **Save dashboard**.
---
`2)` Unit 을 percent(0–100)로
1. 사이드바 상단의 **Search options** 입력칸에 `unit` 이라고 치면 바로 필터됨.
2. **Standard options** 섹션이 보이면, → 그 안의 **Unit** 드롭다운 클릭.
3. 검색창에 `percent` 입력 → **`percent (0–100)`** 선택.
    
> Unit은 수치를 **표시하는 형식**만 바꿔주세요. (실제 계산엔 영향 없음)

 축 범위를 0–100으로 고정
- 같은 사이드바에서 **Axes** 섹션(또는 **Standard options** 안의 **Min / Max**) 열기
- **Min = 0**, **Max = 100** 입력 → 그래프 눈금이 항상 0~100으로 고정돼서 해석이 쉬워짐.
    
---
`3)` Thresholds(가시선) 추가
1. 같은 **Standard options** 섹션 안에 **Thresholds** 가 있어. (없으면 Search에 `thresholds`)
2. **Mode: Absolute** 유지.
3. **Add threshold** 두 번 눌러서 값/색을 지정:
    - 값 **70** → 색은 노랑/주황(경고)
    - 값 **90** → 색은 빨강(심각)
4. Time series 패널에서는 기본이 **선(Line)** 로 표시돼. (선이 안 보이면 Thresholds에서 Style이 _Lines_ 로 되어있는지 확인)
    
> Thresholds 는 **시각적인 가이드라인**입니다.
> 진짜 알림을 보내려면 아래 “Alert”에서 **알림 규칙**을 따로 만들어야 함.

---
`4)` 자잘한 마무리 팁
- **Decimals**(표시 소수점) : Standard options → `0`이나 `1`로 깔끔하게.
- **Legend** : 사이드바 **Legend** 섹션에서 `{{instance}}` 같은 템플릿으로 보기 좋게.
- **Refresh** : 상단 오른쪽 **Refresh** 주기를 5–10s 로 두면 실시간 느낌 OK.
- 저장은 항상 우상단 **Save dashboard**.
---
코어별 CPU 사용률(%)
```
100 - avg by (instance, cpu) (
  rate(node_cpu_seconds_total{mode="idle"}[5m])
) * 100
```

반응을 더 빠르게(민감) 보고 싶으면
```
100 - avg by (instance) (
  irate(node_cpu_seconds_total{mode="idle"}[1m])
) * 100
```

CPU 사용률(%)
```
(1 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100

```

메모리 사용률(%)
```
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
```

디스크 Busy(% 대략)
```
rate(node_disk_io_time_seconds_total{device=~"nvme0n1|sda"}[5m]) * 100
```

네트워크 수신/송신 바이트/초
```
sum by (instance)(rate(node_network_receive_bytes_total[5m]))
sum by (instance)(rate(node_network_transmit_bytes_total[5m]))
```
라벨 필터링은 `{instance="node_exporter:9100"}`처럼 **실제 라벨값**을 써야 합니다.  
(`host1` 같은 가상의 값이면 “No data”. 값은 Explore에서 `sum by(instance)(… )`로 확인)

---
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
- Grafana Dashboard JSON(Export해서 `grafana/` 폴더에 포함)
- 간단 부하 스크립트(`scripts/warmup.sh`)

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
