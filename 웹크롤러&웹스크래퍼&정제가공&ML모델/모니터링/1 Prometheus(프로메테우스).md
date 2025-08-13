#### 모니터링(Web)이란?
웹 서비스나 서버에서 발생하는 상태·성능·이상 징후를 실시간으로 수집·분석해, 서비스가 정상적으로 동작하는지 확인하고 문제를 조기에 발견·대응하는 활동.  
예: 요청 수, 응답 속도, 에러율, CPU·메모리 사용량 등을 시각화해 확인.

###### 개발자가 실무에서 모니터링을 해야 하는 이유
- 장애 예방: 에러율과 지연시간 급증은 장애의 전조
- 성능 튜닝: 느린 API나 DB 쿼리를 찾아서 개선 가능
- 사용량 분석: 트래픽 증가/감소 추세로 서버 자원 계획 세움
- 문제 추적: 특정 시간대에만 발생하는 문제를 로그+지표로 추적 가능

##### Prometheus란?
- 각 애플리케이션이 공개하는 `/metrics` 텍스트 페이지를 주기적으로 긁어와 저장하는 서버(타임시리즈 DB 포함).
- Exporter / Client: 앱(또는 DB/OS)이 지표를 노출하게 만들어주는 도구. (Python 앱은 `prometheus_client`, Django는 `django-prometheus`가 대표적)
- Grafana: Prometheus에 쌓인 지표를 대시보드로 시각화.

![[Pasted image 20250813114809.png]]

시계열 데이터 : 
![[Pasted image 20250813114936.png]]

![[Pasted image 20250813131454.png]]

![[Pasted image 20250813131519.png]]

![[Pasted image 20250813131536.png]]

![[Pasted image 20250813131619.png]]

![[Pasted image 20250813131634.png]]

![[Pasted image 20250813131720.png]]

![[Pasted image 20250813131742.png]]