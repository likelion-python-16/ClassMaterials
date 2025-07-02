
	[feat] django (Day 5)
	-  CSRF 토큰을 위한 getCookie
	-  base.html
	-  axiosInstance
	-  urls 분리
	-  보안및 환경설정 settings.py

`config > settings.py `
``` python
# 개발 시 정적 파일 폴더 설정
STATICFILES_DIRS = [
	BASE_DIR / "static",
]

LOGIN_URL = "/auth/login/"
LOGOUT_REDIRECT_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/todo/list/"

# 이렇게 있으면 todo앱 내부
TEMPLATES = [
	"DIRS": [os.path.join(BASE_DIR, 'todo', 'templates'),]
]

# manage.py와 같은 경로
TEMPLATES = [
	"DIRS": [os.path.join(BASE_DIR, 'templates'),]
]

TIME_ZONE = 'Asia/Seoul' # 한국시간으로 변경
```

`보안설정`
``` bash
# django-environ 설치하기
pip install django-environ
```

`settings.py`
```python
import os, environ # 환경변수 추가

# 가장 윗줄에 있어야 에러가 안남
BASE_DIR = Path(__file__).resolve().parent.parent

# 보안 향상, 코드 재사용, 환경 구분 가능
env = environ.Env(
	DEBUG=(bool, False)
)

# 
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY를 .env로 이동하여 보호
SECRET_KEY = env('DJANGO_SECRET_KEY')
```

`.env 파일을 manage.py경로에 생성`
```python
DJANGO_SECRET_KEY="your-very-secret-key-here"
```

`app 분리관리`
```python
CUSTOM_APPS = [
    'todo',
]

THIRD_PARTY_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

INSTALLED_APPS = CUSTOM_APPS + THIRD_PARTY_APPS
```
---
최종정검
