
	[feat] django (Day 8)
	-  Add login and logout
	-  edit main page


배포
`https://fly.io/`

 `flyctl` CLI 방식이 더 유연하고 안정적
CLI 명령어 흐름으로 배포하면:
1. Dockerfile 커스터마이징 가능
2. `fly.toml` 직접 설정 가능
3. 로컬에서 테스트 후 배포 가능
4. SSH 접속으로 `migrate`, `createsuperuser` 등 실행 가능

![[Pasted image 20250622213135.png]]
flyctl 설치 및 로그인
WSL
```
curl -L https://fly.io/install.sh | sh
```

스크립트는 `~/.fly/bin`에 설치되므로, PATH에 추가해야 합니다.
```
echo 'export PATH="$HOME/.fly/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
---
mac os
```
brew install flyctl
```
맥버전은 path추가 필요없음

버전확인
```
flyctl version
```

settings.py
```python
# Fly 배포용 ALLOWED_HOSTS 설정
APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = [f"{APP_NAME}.fly.dev", "test-todo-list.fly.dev",]

CSRF_TRUSTED_ORIGINS = [
    "https://test-todo-list.fly.dev",  # ← 본인 앱 도메인
]
```

**Gunicorn**은  Django 같은 Python 웹앱을 실제 서버에서 돌리는 프로그램이에요.
"파이썬 웹 애플리케이션(Wsgi)용 고성능 HTTP 서버"입니다.
Gunicorn은 WSGI 서버입니다.
어떤 프로그램이 시작되는 "진입점"
“`wsgi.py`가 Django의 WSGI 엔트리 포인트야”
- 엔트리 포인트는 프로그램이 시작되는 진입점 `wsgi.py`, `main.py`, `index.js` 등
- 엔드 포인트는 클라이언트가 서버에 요청을 보내는 주소
Gunicorn의 역할은? 그 요청을 받아서 Django에 전달하고 응답을 브라우저에 다시 보내주는 역할이에요.

예시로 정리
예: 내가 브라우저에서 아래 주소로 접속한다고 할 때
```
http://myapp.fly.dev/todo/list/
```

일어나는 일은?
1. 브라우저가 `myapp.fly.dev` 서버로 요청을 보냄
2. 요청이 Nginx 또는 fly.io의 로드밸런서를 거침
3. 그 요청이 **Gunicorn**으로 전달됨 ← 이게 WSGI 서버
4. Gunicorn이 요청을 Django의 `wsgi.py` 진입점으로 전달
5. Django가 DB에서 데이터를 가져오고
6. Gunicorn이 결과를 받아서 브라우저에 응답

---
✅ 비유
Gunicorn은 마치 음식점에서 전달자 역할을 하는 주방 총괄 관리자입니다.
손님(브라우저)이 메뉴를 요청하면,  
Gunicorn이 주방(Django)에 전달하고, 요리(DB 처리)를 끝내고, 다시 손님에게 음식(응답)을 내보내요.  직접 서빙하는 건 아니지만, 중심 역할을 하죠.

---
Gunicorn, requirements.txt 생성
```
pip install gunicorn
pip freeze > requirements.txt
```

설치 후 로그인:
```
flyctl auth login
```

로그인 확인
```
flyctl auth whoami
```

![[Pasted image 20250622220209.png]]

결제 수단 등록 (필수)
https://fly.io/dashboard/anne-lee/billing
- 카드는 등록만 해도 됩니다.
- 기본 배포 (1GB RAM, shared CPU 1x)는 무료 크레딧 내에서 대부분 커버됨
- 실제 과금은 발생하지 않도록 Fly에서 확인해줍니다.

![[Pasted image 20250622221846.png]]

![[Pasted image 20250622221854.png]]

![[Pasted image 20250622222125.png]]

로그인이 잘되었다면 런처를 실행:
```
flyctl launch
```

Do you want to tweak these settings before proceeding? (y/N) N
`N`을 입력하면 Fly가 기본 설정으로 `fly.toml` 파일과 필요한 리소스를 자동 생성합니다.
Fly.io는 2024년 말부터 무료 티어만으로는 머신(서버) 실행이 제한됨

Fly.io / Render / Railway
커스텀 DB, 로컬스토리지, 사설망 필요: AWS EC2 / Lightsail 라이트세일
쿠버네티스 기반 확장성 필요:GKE, EKS 등 클라우드 클러스터
- EC2: 고급자용. 네트워크, 보안, 디스크 모두 직접 설정해야 함
- Lightsail: 워드프레스, Django, Node.js 등을 클릭 몇 번으로 배포 가능


다시 실행해야 하는경우는 아래 명령어:
```
flyctl deploy
```

배포 주소 : https://test-todo-list.fly.dev/

서버 접속 (ssh)
```
flyctl ssh console
```

마이그레이션 실행
```
root@784e11ef65e258:/code# 
python manage.py migrate
```

```
python manage.py createsuperuser
```

https://test-todo-list.fly.dev/admin/

![[Pasted image 20250622222939.png]]

403 CSRF verification failed 오류는 Django 보안 기능인 CSRF 보호가 Fly.io 서버에서 동작할 때 추가 설정이 누락되어 발생
```
CSRF_TRUSTED_ORIGINS = [
    "https://test-todo-list.fly.dev",  # ← 본인 앱 도메인
]

import os

APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = [
    f"{APP_NAME}.fly.dev",
    "test-todo-list.fly.dev",  # ← 직접 주소로도 추가
]
```

templates/registration/logged_out.html 임시로 만들어 놓는다.
```html
{% extends "base.html" %}
{% block content %}
  <h2>성공적으로 로그아웃되었습니다.</h2>
  <a href="/">홈으로 가기</a>
{% endblock %}
```

```python
path("accounts/", include("django.contrib.auth.urls")),
```

변경 후 반드시 재배포
```
flyctl deploy
```

```
flyctl ssh console
```

```
python manage.py migrate
python manage.py createsuperuser
```

https://test-todo-list.fly.dev/admin/
https://test-todo-list.fly.dev/

서버에러500이 날때 settings.py에 설정확인
```
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

해결방법
```
python manage.py collectstatic --noinput
```

![[Pasted image 20250622224628.png]]


앱삭제
```
fly apps list
fly apps destroy [앱이름]
```


```
fly secrets set SECRET_KEY= '장고키'
```
