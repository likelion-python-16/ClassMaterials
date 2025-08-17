첫번째 방법: Grafana 알림으로 Discord 보내기
>이미 Grafana를 쓰고 있으니 이게 보통 제일 쉬워요.

- **Discord Webhook URL 만들기**
    - 디스코드 서버 → **Server Settings → Integrations → Webhooks → New Webhook**
    - 보낼 **채널 선택** 후 **Webhook URL** 복사
        
- **Grafana에 Contact point 추가**
    - Grafana → **Alerting → Contact points → New contact point**
    - 유형: **Discord**(버전에 따라 **Webhook** 선택 후 URL 붙여넣기)
    - Webhook URL에 방금 복사한 주소 붙여넣고 저장
        
- **Notification policy 연결**
    - **Alerting → Notification policies**에서 기본 정책에 방금 만든 Contact point를 연결
    - 라벨(예: `severity=warning|critical`)별로 라우팅도 가능
        
- **알림 규칙 만들기(예시 3개)**
    - Grafana → **Alerting → Alert rules → New alert rule**
    - Data source: **Prometheus**
    - **5xx 에러율 > 1% (5m)**
```
100 *
( sum(rate(fastapi_request_count_total{endpoint!="/metrics", status_code=~"5.."}[5m])) or vector(0) )
/
clamp_min(sum(rate(fastapi_request_count_total{endpoint!="/metrics"}[5m])), 1)
```
-  Condition: 위 쿼리 결과 is above 1
- For: **5m**

p95 > 800ms (5m)
```
1000 *
histogram_quantile(
  0.95,
  sum by (le) (rate(fastapi_request_latency_seconds_bucket[5m]))
)
```
- (끝에 `*1000` 해서 ms로 변환)
- **Condition**: **is above 800**, **For: 5m**

메모리 여유 < 500MB (5m)
```
node_memory_MemAvailable_bytes / 1024 / 1024
```
- Condition: is below 500, For: 5m
각 규칙의 **Annotations**에 대시보드 링크/Runbook URL/요약문 넣기
---
 두번째 방법: Prometheus Alertmanager → Discord (Webhook 브리지)
> Alertmanager를  쓰거나, Prometheus 쪽에서 라우팅/사일런스를 통일하고 싶을 때.

- Alertmanager는 Slack/Email/Webhook** 등은 기본 지원하지만 Discord는 기본 리시버가 없음.
    
- 대신 Webhook 리시버를 하나 두고(예: 작은 브리지 서비스), Alertmanager가 보내는 JSON을 Discord Webhook 포맷으로 변환해 Discord Webhook URL로 다시 POST하면 됩니다.

alertmanager.yml
```
route:
  receiver: discord
  group_by: ['alertname']
receivers:
  - name: discord
    webhook_configs:
      - url: http://discord-bridge:8080/alert  # 내가 띄운 브리지
```
- 브리지(예: FastAPI/Express)에서 Alertmanager payload를 받아  
    `{"content": "**[{{$labels.severity}}] {{$labels.alertname}}**\n{{$annotations.summary}}"}`  
    형태로 **Discord 웹훅 URL**에 POST.
    
> 장점: 팀이 Alertmanager를 표준으로 쓰면 라우팅/사일런스/템플릿을 한 군데에서 관리.

---
 알람 & SLO를 “현업 스타일”로 만들 때 팁
- **의도와 기준을 규칙에 녹이기**
    - 예: “고객 영향” 기준만 알림 → 5xx%/p95 중심, **For 5m**로 잡음(스파이크 노이즈 제거)
        
- **라벨링**
    - `severity=warning|critical`, `service=api`, `team=backend` 라벨을 붙여 라우팅/필터링
        
- **메시지 템플릿(Annotations)**
    - `summary`: 짧게(한 줄)
    - `description`: 원인 가설/확인 단계
    - `dashboard`: 대시보드 링크
    - `runbook`: 대응 문서 링크
        
- **소음 억제**
    - 동일 경보 **그룹/딜레이**(예: group_wait 30s, group_interval 5m)
    - **Silence** 규칙(배포창/야간 점검)
        
- **SLO/에러버짓과 연결**
    - SLI: 5xx%, p95
    - SLO: “5xx < 1%, p95 < 800ms(30일)”
    - 에러버짓 소모율이 급증하면 별도 알림


