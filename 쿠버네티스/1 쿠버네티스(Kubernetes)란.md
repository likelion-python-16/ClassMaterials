쿠버네티스(Kubernetes)는 다수의 컨테이너를 효율적으로 배포, 확장 및 관리하기 위한 오픈소스 시스템입니다.

쿠버네티스는 Docker Compose와 비슷한 느낌을 가지고 있다.  
Docker Compose도 다수의 컨테이너를 쉽게 관리하기 위해 활용하기 때문입니다.
머릿속에서 쿠버네티스의 대략적인 이미지를 그릴 때는 Docker Compose의 확장판이라고 생각하면 편합니다.

### ✅ 쿠버네티스의 장점

- 컨테이너 관리 자동화 (배포, 확장, 업데이트)
- 부하 분산 (로드 밸런싱)
- 쉬운 스케일링
- 셀프 힐링(Self-Healing)

쉽게 풀어쓴 쿠버네티스 사용 이유
1. **배포(Deployment)를 자동화**
    - 한 번 `kubectl apply` 해두면, 쿠버네티스가 알아서 파드를 띄워줌
    - 버전 업데이트도 **롤링업데이트**로 무중단 배포 가능
        
2. **서버 장애 자동 복구 (Self-healing)**
    - 파드가 죽거나 노드가 장애 나면 → 쿠버네티스가 자동으로 새 파드를 띄움
    - 👉 “서버가 죽어도 서비스가 멈추지 않게”
        
3. **부하 분산 & 확장성**
    - 트래픽이 많아지면 `replicas`를 늘리거나 HPA로 자동 스케일링
    - 요청은 Service가 여러 파드에 자동 분산 (로드밸런싱)
        
4. **운영 편의성**
    - 설정(ConfigMap/Secret), 네트워크(Service/Ingress), 모니터링(HPA) 등이 모두 통합 관리
    - 개발자/운영자가 “원하는 상태”만 선언하면 → 클러스터가 알아서 유지

---
### ✅ 파드(Pod)란?

도커에서는 하나의 프로그램을 실행시키는 단위를 컨테이너라고 주로 불렀습니다.  쿠버네티스에서는 하나의 프로그램을 실행시키는 단위를 파드(Pod)라고 부릅니다.

따라서 파드(Pod)는 일반적으로 쿠버네티스에서 하나의 프로그램을 실행시키는 단위라고 기억해두시면 이해하시기 편합니다.

- 파드는 쿠버네티스에서 가장 작은 단위입니다.
- 일반적으로 하나의 파드는 하나의 컨테이너를 가집니다.  
    (예외적으로 하나의 파드가 여러 개의 컨테이너를 가지는 경우도 있습니다.)

> **참고**: 여기서 말하는 컨테이너는 “Docker의 컨테이너”를 뜻합니다.

![[Group 465.png]]
- 결제 서버 두 개가 실행되었습니다.  
    = 결제 서버 파드(Pod) 두 개가 실행되었습니다.
    
- 결제 서버 하나가 중지되었습니다.  
    = 결제 서버 파드(Pod) 하나가 중지되었습니다.
    
- 업로드 서버를 하나 실행해 보겠습니다.  
    = 업로드 서버 하나를 파드(Pod)로 실행하겠습니다.

### ✅ 쿠버네티스도 도커처럼 이미지를 기반으로 파드(Pod)를 띄워 실행 시킨다.
![[Group 466.png]]

---
## 쿠버네티스 오브젝트(Object) & 리소스(Resource) 기본 개념

🔹 쿠버네티스 클러스터 기본 구조
- 클러스터(Cluster) → 전체 놀이터 (쿠버네티스가 관리하는 큰 틀)
- 노드(Node) → 실제 서버(가상머신/물리머신), 파드가 올라가는 실행 환경
    
---
🔹 워크로드(Workload) 리소스
- 파드(Pod) → 가장 작은 실행 단위 (컨테이너 묶음)
- 디플로이먼트(Deployment) → 파드의 수명 관리 (복제, 업데이트, 자가복구)
- HPA(HorizontalPodAutoscaler) → 부하에 따라 파드 개수를 자동으로 조정
    
---
🔹 네트워킹 리소스
- 서비스(Service) → 파드의 고정된 접근 주소 제공 (로드밸런싱 포함)
- 인그레스(Ingress) → 외부 HTTP(S) 트래픽을 받아 내부 서비스로 라우팅
    
---
🔹 설정/보안 리소스
- ConfigMap → 환경설정값 주입 (비민감 데이터)
- Secret → 민감정보 주입 (비밀번호, 토큰 등)
---
kubernetes [https://kubernetes.io/ko/docs/concepts/overview/components/](https://kubernetes.io/ko/docs/concepts/overview/components/)
![[Pasted image 20250910114705.png]]

쿠버네티스, 위 이미지 요약
- 클러스터 = 컨트롤 플레인(두뇌) + 노드(손발)
- 파드(Pod)는 컨테이너가 들어있는 가장 작은 실행 단위(보통 1컨테이너=1파드).
- 컨트롤 플레인은 “원하는 상태”를 기억하고, 파드를 어느 노드에 띄울지 정하고, 죽으면 다시 살립니다(셀프 힐링).
    
---
이미지 속 아이콘을 쉬운 말로

컨트롤 플레인(좌측 파란 박스) – “두뇌”
- **api (kube-apiserver)**: 쿠버네티스의 정문/수위실. `kubectl` 명령이 여기로 들어와요.
- **etcd**: 클러스터 상태를 저장하는 메모장(DB). “원하는/현재 상태”가 여기에 기록됨.
- **sched (kube-scheduler)**: “이 파드는 어떤 노드에 배치?” 자리 배치 담당.
- **c-m (kube-controller-manager)**: 목표 상태와 실제 상태를 맞춰주는 집사.
    - 예) 레플리카 수 유지, 잡 실행, 엔드포인트 연결, 서비스어카운트 생성 등.
- **c-c-m (cloud-controller-manager)**: 클라우드랑 통역사 역할.
    - 로드밸런서 만들기, 노드/경로 처리 등 클라우드 API와 연동.
    - 로컬(minikube) 학습에선 보통 크게 신경 안 써도 됨.
        
노드(오른쪽 회색 박스들) – “손발”
- kubelet: 노드 관리자. “이 파드 실행하라” 명령을 받아 컨테이너를 띄우고 건강 체크.
- k-proxy (kube-proxy): 네트워크 라우터. Service 가상 IP로 들어온 트래픽을 파드에 연결.
- 컨테이너 런타임: 실제 컨테이너를 돌리는 엔진(containerd, CRI-O 등).
    
클라우드 아이콘
- Cloud provider API: 클라우드의 로드밸런서/디스크 등을 자동으로 만들어달라고 요청하는 창구(있으면 c-c-m이 사용).
    
---
“디플로이먼트를 적용하면 무슨 일이?” (6단계 스토리)
1. `kubectl apply -f deployment.yaml` → API Server가 접수하고 etcd에 기록.
2. Scheduler가 파드를 올릴 노드를 결정.
3. 해당 노드의 kubelet이 이미지를 받아 파드를 실행, 헬스체크 연결.
4. kube-proxy가 Service(가상 IP)로 온 트래픽을 파드로 라우팅.
5. 필요하면 Cloud Controller가 로드밸런서 같은 클라우드 리소스를 생성.
6. 파드가 죽으면 Controller Manager가 새로 띄워 목표 상태를 유지(셀프 힐링).
    
---
꼭 알아둘 리소스 6개(처음 시작 세트)
- Pod: 컨테이너가 들어있는 최소 실행 단위
- Deployment: 파드 개수 유지/업데이트/자가복구(운영 표준)
- Service: 파드 묶음에 고정 주소 부여(ClusterIP/NodePort/LoadBalancer)
- Ingress: 외부 HTTP(S) 정문(도메인/경로 라우팅, NGINX 컨트롤러 필요)
- ConfigMap / Secret: 환경설정 / 민감값을 이미지 밖에서 주입
- **HPA**: 부하에 따라 파드 자동 확장(metrics-server 필요)
    
> 처음엔 `Deployment + Service` 만으로 시작 → 익숙해지면 `Ingress → HPA → ConfigMap/Secret` 순서로 확장하세요.

---
Docker Compose와의 감각적 매핑
- Compose의 `services` → K8s의 Deployment + Service
- `ports` → Service + Ingress
- `environment` → ConfigMap/Secret
- `scale` → `replicas` + HPA
    
---
애드온(있으면 좋은 것)
- DNS: 서비스 이름으로 통신하려면 필수(클러스터 기본 제공)
- 대시보드: 웹 UI
- metrics/logging 스택: Prometheus/Grafana, 중앙 로그 등(다음 단계)
    
---
시작 체크 명령어(진짜 자주 씀)
```
kubectl get nodes
kubectl get pods -A
kubectl get deploy,svc,ingress -A
kubectl logs -f deploy/<name> -n <ns>
kubectl rollout restart deploy/<name> -n <ns>
kubectl top pods -n <ns> # metrics-server 필요
```

`kubectl`은 쿠버네티스(Kubernetes) 클러스터를 제어하기 위한 공식 CLI 도구입니다. 터미널에서 쿠버네티스 관련 명령을 실행할 때 항상 접두어처럼 `kubectl`을 붙입니다.

- `kubectl get nodes`  
    클러스터에 연결된 노드(서버) 목록 보기. → “클러스터가 살아있나” 1차 확인.
- `kubectl get pods -A`  
    모든 네임스페이스의 파드 현황. (`-n app-dev`로 특정 네임스페이스만 볼 수도 있음)
- `kubectl get deploy,svc,ingress -A`  
    디플로이먼트/서비스/인그레스만 필터링해서 한 번에 보기.
- `kubectl logs -f deploy/<name> -n <ns>`  
    디플로이먼트가 관리하는 파드들의 로그 스트리밍. (컨테이너 여러 개면 `-c <container>`)
- `kubectl rollout restart deploy/<name> -n <ns>`  
    롤링 재시작 트리거(이미지 다시 풀거나 환경변수 반영 시).  
    이어서 `kubectl rollout status deploy/<name> -n <ns>`로 진행상황 확인.
- `kubectl top pods -n <ns>`  
    파드의 CPU/메모리 실시간 지표(HPA 확인용).  
    ↳ metrics-server
     애드온이 켜져 있어야 동작: `minikube addons enable metrics-server`