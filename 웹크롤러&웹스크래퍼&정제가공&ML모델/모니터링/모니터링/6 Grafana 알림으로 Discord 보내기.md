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

---
### **Grafana Alerting**

- Grafana 대시보드에서 직접 Alert rule을 만들고,
- Contact point(Discord Webhook 등)와 Notification policy를 연결해서 알림 전송
- 이 경우 Prometheus는 데이터 소스 역할만 합니다.
- Grafana 내부 DB(sqlite)에 룰과 contact point 설정이 저장됩니다.


`1.` Alertmanager 설치
Prometheus 단독으로는 알람을 보낼 수 없고, **Alertmanager**라는 모듈이 필요합니다.

Docker 실행
```bash
docker run -d --name alertmanager \
  -p 9093:9093 \
  -v $(pwd)/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager
```

`2.` Discord Webhook 만들기
1. 디스코드 서버 → `서버 설정` → `연동` → `웹후크`
2. 웹후크 URL을 복사합니다 (예: `https://discord.com/api/webhooks/...`).

서버설정
![[Pasted image 20250818132843.png]]

연동/웹후크만들기
![[Pasted image 20250818133708.png]]

웹후크 만들기
![[Pasted image 20250818133846.png]]

웹후크 url을 복사합니다.
```
https://discord.com/api/webhooks/1406859561033400460/Zpk7HDWh74GBd.............................
```

설치 위치 잡기 (한 번만)
Alertmanager 설치 (WSL)
```bash
# 홈으로 이동
cd ~

# 알림매니저 받기 (버전은 예시, 최신 안정버전 쓰세요)
wget https://github.com/prometheus/alertmanager/releases/download/v0.27.0/alertmanager-0.27.0.linux-amd64.tar.gz
tar xvf alertmanager-0.27.0.linux-amd64.tar.gz
cd alertmanager-0.27.0.linux-amd64
```
폴더는 홈(`~`)에 두는 걸 권장하지만, 프로젝트 폴더 안에 둬도 작동엔 문제 없습니다.

Grafana 실행
```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```
- 접속: [http://localhost:3000](http://localhost:3000)
- 로그인: `admin / admin` (처음에 비번 변경 필요)

Grafana에서 Prometheus 연결
- **Settings → Data sources → Add data source → Prometheus**
- URL: `http://prometheus:9090` (Docker가 아닌 WSL이라면 `http://localhost:9090`)
- Save & test → “Data source is working” 확인

![[Pasted image 20250818141930.png]]

![[Pasted image 20250818142005.png]]

![[Pasted image 20250818142319.png]]

입력해야 하는 부분 (최소 설정)
1. **Name**
    - `discord-alert`
    - (알림 대상 구분용 이름 → 자유롭게 지어도 됨)
2. **Integration**
    - `Webhook` 
3. **URL**
    - 디스코드 서버에서 복사해온 **Webhook URL**
    - 예:
`https://discord.com/api/webhooks/140685956103304060/ZpX7HDW74GBd...`
4. **HTTP Method**
    - `POST` (기본값 그대로 둠)
5. **HTTP Headers**
    - Discord는 별도의 Auth가 필요 없음 →  
        👉 여기서는 아무것도 입력하지 않아도 됨
6. 나머지 항목은 건드리지 않아도 됩니다.

**Test → Send test notification** 클릭시 디코에 메시지가 잘 가는지 확인합니다.
![[Pasted image 20250819174607.png]]

---
Notification policies 설정
![[Pasted image 20250818142606.png]]

Default policy 수정
![[Pasted image 20250818142846.png]]

여기서 드롭다운을 눌러서 **discord-alert** (아까 만든 Contact point 이름) 선택
![[Pasted image 20250818142931.png]]
update 하면 끝!

---
일부러 조건을 만족시켜서 Discord에 알림이 오는지 확인

알람 룰 생성하기 (테스트용)
1. Grafana 좌측 메뉴 → **Alerting → Alert rules → New alert rule** 클릭
2. 설정:
    - **Name**: `Test CPU Alert`
    - **Data source**: Prometheus
    - **Query (PromQL)**: 예시

Alert rules
![[Pasted image 20250818143225.png]]

New alert rule 클릭
![[Pasted image 20250818143311.png]]

![[Pasted image 20250818145708.png]]

![[Pasted image 20250818145725.png]]

저장 위치 (Evaluation Group & Folder)
![[Pasted image 20250818145818.png]]

**Evaluation behavior (평가 동작)** 설정
얼마나 자주 이 Alert Rule을 실행해서 조건을 확인할지"를 그룹으로 관리하는 기능
![[Pasted image 20250818145954.png]]
- 오른쪽의 **`+ New evaluation group`** 버튼을 눌러서 새 그룹을 만드세요.
- 이름 예시: `default-eval` 또는 `cpu-check`
- Interval (평가 주기): `1m` (1분마다 이 룰을 검사) 추천
- Configure no data and error handling (선택)
- Prometheus가 데이터 못 가져올 때 알람을 보낼지 말지 선택 가능.
- 보통 테스트 단계에서는 기본값 유지하세요.


지금은 테스트 단계니까 `+ New evaluation group` 눌러서
- Name: `cpu-check`
- Interval: `1m`
![[Pasted image 20250818150027.png]]

데이터가 안 들어오거나 null인 경우 어떻게 처리할지입니다.
![[Pasted image 20250818150200.png]]
Alert state if no data or all values are null
-  No Data (기본값) → 그냥 상태를 `No Data`로 표시 (알람은 안 울림)
- Alerting → 데이터를 못 가져와도 알람을 발생
- OK → 데이터를 못 가져오면 그냥 정상으로 취급
👉 추천: No Data  
(데이터 수집기 문제 때문에 괜히 Discord에 알람이 폭주하는 걸 방지)

Alert state if execution error or timeout
Prometheus 쿼리 실행 실패나 Timeout일 때 상태를 어떻게 할지입니다.
- **Error** (기본값) → 상태를 `Error`로 표시 (알람은 아님)
- **Alerting** → 오류를 알람으로 보냄
- **OK** → 그냥 무시
👉 추천: **Error**  
(실제로 에러 상황과 모니터링 알람은 구분하는 게 좋아요)

5. Configure notifications
![[Pasted image 20250818150634.png]]
- Contact point: 이미 `discord-alert` 로 선택했으니까 OK
- Webhook URL도 자동으로 따라왔으니 건드릴 필요 없음
👉 여기까지가 필수 설정이에요.
---
6. Configure notification message
이건 Discord에 표시될 메시지 내용을 커스터마이즈하는 부분입니다.
- **Summary (optional)**: 알람의 제목 (예: `CPU usage is too high!`)
- **Description (optional)**: 추가 설명 (예: `CPU usage exceeded threshold for more than 1 minute.`)
- **Runbook URL (optional)**: 문제가 발생했을 때 참고할 문서나 링크 넣는 용도 (보통 내부 위키, Notion, GitHub README 등)

Summary + Description을 넣어두면 알람이 더 예쁘게 옵니다.  
예를 들어:
- Summary → `🚨 CPU Alert`
- Description → `CPU usage over 80% for 1m on {{ $labels.instance }}`

Grafana는 Go 템플릿을 쓰기 때문에, `{{ $labels.instance }}` 같은 변수를 넣으면 실제 서버 이름(IP)이 표시돼요.

---









