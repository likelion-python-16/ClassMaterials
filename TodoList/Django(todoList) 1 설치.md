🔗 [todoList](https://github.com/handgonpo/todoList/commit/9bad7b32518b2e0b8326ef3f7f125fba990a61d8)

	[feat] django (Day 1)
	- context data 
	- Template Tags 
	- Template for 
	- Template if endif

🔗 [[Django_basic/Django_공식문서-깃허브업뎃용/1. 공식문서를 통한 장고설치/1. 공식문서를 통한 장고 설치]]
🔗 [[Django_basic/Django_공식문서-깃허브업뎃용/2. Part1/Part 1]]

---
✅ 1단계: 프로젝트 디렉터리로 이동: `mysite/`는 `startproject` 명령으로 생성한 프로젝트 루트입니다.
```bash
# 디렉터리 생성
mkdir todoList

# 해당 디렉터리로 이동
cd todoList

# 가상환경 설정
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install django
pip install djangorestframework
```
---
✅ 2단계: 프로젝트 생성 & 앱 생성
```bash
# Django 프로젝트 생성 (주의: . 을 붙이면 현재 폴더에 생성됨)
django-admin startproject config .

# 앱 생성 (예: 할 일 관리용 앱 todo)
python manage.py startapp todo
```
---
✅ 생성 후 구조
```python
todoList/
├── config/             # ← settings.py 있는 메인 프로젝트
├── todo/               # ← 새로 만든 앱
├── manage.py
├── venv/
└── requirements.txt
```
---
✅ 용어 설명

| 용어              | 뜻                                               |
| --------------- | ----------------------------------------------- |
| 라우팅 (Routing)   | 사용자가 웹 주소에 접근했을 때, 어떤 함수(또는 화면)가 실행될지 길을 지정하는 것 |
| **path()**      | 특정 URL 주소에 대해 실행할 내용을 설정하는 Django의 함수           |
| **include()**   | 다른 앱(`todo`)의 URL들을 불러와서 현재 URL에 붙이는 역할         |
| **urlpatterns** | 주소와 실행할 기능들을 모아둔 URL 목록                         |

---
`config/settings.py`
```python
INSTALLED_APPS = [
    'todo',
    'rest_framework',
]
```

`todo > models.py`
``` python
from django.db import models

class Todo(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	complete = models.BooleanField(default=False)
	exp = models.PositiveIntegerField(default=0)
	completed_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
```

`DB테이블 생성`
```bash
python manage.py makemigrations
python manage.py migrate
```

`관리자생성`
```bash
python manage.py createsuperuser
```
---
✅ 라우팅(Routing) 
`config > urls.py`
```python
from django.contrib import admin 
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
	path('admin/', admin.site.urls),
	path("todo/", include("todo.urls")), 
	path('', lambda request: redirect('todo_List')),
]
```
---
`todo > urls.py`
```python
# todo > urls.py
from django.urls import path
from . import views

# 127.0.0.1:8000/todo/
urlpatterns = [
	path("list/", views.todo_list, name="todo_List"), 
	#데이터 작동 테스트용
]
```
---
`todo > views.py` 테스트용
```python
from django.shortcuts import render
from .models import Todo
from django.views import View 

def todo_list(request): # 테스트용 함수형
	todos = Todo.objects.all()
	return render(request, "todo/todo.html", {"todos": todos})

class TodoListView(View): # 클래스형
   def get(self, request):
       return render(request, "todo/create.html")


from django.views.generic import ListView

class TodoListView(ListView): # 제너릭뷰
    model = Todo
    template_name = "todo/todo.html"  # 기본값: todo_list.html
    context_object_name = "todos"     # 기본값: object_list
```

`todo/admin.py`
```python
from django.contrib import admin
from .models import Todo

admin.site.register(Todo)
```

`admin에 접속하여 데이터를 입력한다.`

`config/settings.py`
```python
import os

TEMPLATES = [
	"DIRS": [os.path.join(BASE_DIR, "templates")],
]

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

LANGUAGE_CODE = 'ko-kr'
```

`templates > todo > todo.html`
```html	 
{% for todo in todos %}
    <p>{{ todo.name }}</p>
    <p>{{ todo.description }}</p>  
    <p>{{ todo.complete }}</p>
    <p>{{ todo.created_at }}</p>
    <p>-------------------------</p>

    {% if todo.description %}
        <p>{{ todo.description }}</p>
    {% else %}
        No description
    {% endif %}
        <p>{{ todo.complete }}</p>
        <p>{{ todo.created_at }}</p>
{% endfor %}
```

`todo > admin.py`
``` python
from django.contrib import admin
from .models import Todo

admin.site.register(Todo) # 선택

@admin.register(Todo) # 선택
class TodoAdmin(admin.ModelAdmin):
	list_display = (
		"__str__",
		"created_at",
		"updated_at",
	)
```

`.gitignore`
```python
# Python 기본 캐시 및 가상환경 파일 제외
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd

# 환경 변수 파일 (보안 중요)
.env
# 개발중에만 사용

# 데이터베이스 파일 제외 (SQLite 등)
db.sqlite3
*.sqlite3

# Django 마이그레이션 캐시 제외
**/migrations/*.pyc
**/migrations/*.py
!**/migrations/__init__.py

# 로그 파일 제외
*.log
*.out
*.err

# 미디어 및 정적 파일 (수동 업로드 방지)
# media/
# staticfiles/
# static/
node_modules/

# VS Code 및 IDE 설정 파일 제외
.vscode/
.idea/
*.sublime-workspace

# Docker 관련 파일 제외 (사용할 경우)
docker-compose.override.yml
```

`README.md`
``` README.md
	# todoList
	이 프로젝트는 Django 기반으로 만든 todoList입니다.
	
	## 주요 기능
	- 회원가입/로그인
	- 게시글 CRUD
	
	## 사용 기술
	
	### 백엔드
	- Python, Django, Django ORM, Django Template Engine
	- Django REST Framework (DRF)
	- SQLite3 (개발용 DB)
	
	### 프론트엔드
	- HTML5, CSS3, Bootstrap
	- JavaScript, jQuery, Axios
	- Django Template Tags
	
	### 테스트/디버깅
	- Insomnia
	
	### 배포/운영
	- AWS EC2
	- Docker, docker-compose
	- Nginx, Gunicorn
```
