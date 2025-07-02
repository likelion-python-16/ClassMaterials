
	[feat] django (Day 2)
	- rest API install 
	- serializers 
	- apis 
	- imsomnia

	- 파일 분리 : 템플릿 렌더링과 API를 분리해서 가독성과 유지보수를 
	좋게 하려는 목적
	- 단: 반드시 apis.py로 파일명을 만들 필요는 없다. views.py에 
	작성해도 된다.
---
###### 🔹 목록보기

`todo > urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
	path("list/", views.TodoListView.as_view(), name="todo_List"),
    # 실제 작동용 list
]
```

`todo > serializers.py`
```python
from rest_framework.serializers import ModelSerializer
from .models import Todo

class TodoSerializer(ModelSerializer):
	class Meta:
		model = Todo
		fields = "__all__" # 모델의 모든 필드를 자동으로 직렬화합니다
        
        fields = [
            "name",
            "description",
            "complete",
            "exp",
            "completed_at",
            "created_at",
            "updated_at"
        ]
        exclude = ["created_at", "updated_at"]
        # **모든 필드를 기본 포함시키고** → 특정 필드만 제외하고 싶을 때
```
사용 안하고 싶은 필드는 안쓰면 자동 제외가 된다.
일부 필드만 사용하고 싶다` fields = ["필드1", "필드2"]`
거의 모든 필드를 쓰는데 몇 개만 빼고 싶다 `exclude = ["뺄_필드1", "뺄_필드2"]`

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

INSTALLED_APPS = [
	'rest_framework',
]
```
DRF가 HTML 렌더링 대신 JSON만 반환
`http://127.0.0.1:8000/todo/api/list/`

`todo/views.py`
```python
from django.shortcuts import render
from .models import Todo
from django.views.generic import ListView
from django.urls import reverse_lazy

# 목록 조회
class TodoListView(ListView):
    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"
    ordering = ['-created_at']
    success_url = reverse_lazy('todo_List')
```

`templates/base.html`
```html
{% load static %} 
<!DOCTYPE html>
<html lang="ko">
<body>
	{% block content %}{% endblock %}
</body>
</html>
```

`todo/list.html`
```html
{% extends "base.html" %}
{% load static %}
{% block content %}

<div class="todocontainer"> 
    {% for todo in todos %}
        <div class="todo-item">
            <p><strong>이름:</strong> {{ todo.name }}</p>
            <p><strong>설명:</strong> {{ todo.description }}</p>
            <p><strong>완료 여부:</strong> {{ todo.complete }}</p>
            <p><strong>작성일:</strong> 
            {{ todo.created_at|date:"Y-m-d H:i" }}</p>
            
            <hr>
        </div>
    {% empty %}
        <p>등록된 할 일이 없습니다.</p>
    {% endfor %}
</div>
<button class="todoCreate" id="createBtn">Todo 등록하기</button>

<script>
    document.addEventListener("DOMContentLoaded", function () {
        console.log("create loading");
    });
		    
	document.getElementById("createBtn").addEventListener
	("click", () => {
		//window.location.href = "/todo/create/"; # 라우터주소
		console.log("createBtn click")
	});

</script>
{% endblock %}
```
`("click", () => { ... })` 이 부분은 자바스크립트의 화살표 함수(Arrow Function) 문법입니다.

화살표 함수 문법:
```javascript
() => {
  // 클릭 시 실행할 코드
}
```
- `()` : 매개변수 (없으면 비워둠)
- `=> { ... }` : 함수의 본문
- 화살표 함수는 `function()` 키워드보다 **간결한 문법**입니다.

동일한 의미의 일반 함수 방식:
```javascript
document.getElementById("createBtn").addEventListener("click", function () {
    window.location.href = "/todo/create/"; # 클릭후 이동할 URL
    console.log("createBtn click");
});
```

`todo/urls.py`
```python
from . import api_views

path("api/list/", api_views.TodoListAPI.as_view(), name="todo_api_list"),
```

`todo > api_views.py` 
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer
from .models import Todo
from rest_framework import status

# 전체보기
class TodoListAPI(APIView):
	def get(self, request):
		todos = Todo.objects.all() 
		serializer = TodoSerializer(todos, many=True)
		return Response(serializer.data)
```
/todo/list/  전체 Todo 목록 조회
`http://127.0.0.1:8000/todo/api/list/`

---
###### 🔹 생성하기

`todo/urls.py`
```python
# 탬플릿View
path("create/", views.TodoCreateView.as_view(), name="todo_Create"),

# APIView
path("api/create/", api_views.TodoCreateAPI.as_view(), name="todo_api_create"),
```

`todo/views.py`
```python
from django.views.generic import ListView, CreateView

# 생성
class TodoCreateView(CreateView):
    model = Todo
    fields = ['name', 'description', 'complete', 'exp']
    template_name = "todo/create.html"
    success_url = reverse_lazy('todo_List')
```

`todo/api_views.py`
```python
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer
from .models import Todo

# 생성하기
class TodoCreateAPI(APIView):
	def post(self, request):
		serializer = TodoSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		todo = serializer.save()
		return Response(TodoSerializer(todo).data,
		status=status.HTTP_201_CREATED)
```

`templates/create.html`
```html
{% extends "base.html" %}
{% load static %}
{% block content %}
<div class="container">
    <h2>Create a New Todo</h2>
        <div>
            <label for="name">Name:</label>
            <input type="text" name="name" id="name">
        </div>

        <div>
            <label for="description">Description:</label>
            <textarea name="description" id="description">
            </textarea>
        </div>

        <div>
            <label for="complete">Complete:</label>
            <input type="checkbox" name="complete" id="complete">
        </div>

        <div>
            <label for="exp">Experience Points:</label>
            <input type="number" name="exp" id="exp" min="0">
        </div>

        <button type="submit" id="todoCreate">Create</button>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function () {
        console.log("create loading")
    });
</script>
{% endblock %}
```

/todo/create/  새로운 Todo 생성
`http://127.0.0.1:8000/todo/api/create/`
`TodoCreateAPI`  `POST`

`테스트 데이터 Imsomnia`
```
{
		"name": "멋쟁이호랑이처럼",
		"description": "설명을 작성해줘",
		"complete": false,
		"exp": 10
	}
```
----
###### 🔹 상세보기

`todo/urls.py`
```python
# 탬플릿View
path("detail/<int:pk>/", views.TodoDetailView.as_view(), name="todo_Detail"),

# APIView
path("api/retrieve/<int:pk>/", api_views.TodoRetrieveAPI.as_view(), name="todo_api_retrieve"),
```

`todo/views.py`
```python
# 상세보기
class TodoDetailView(DetailView):
    model = Todo
    template_name = "todo/detail.html"
    context_object_name = "todo"
```

`api_views.py`
```python
# 상세보기
class TodoRetrieveAPI(APIView):
    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error":"해당하는 todo가 없습니다."},
            status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
```

`templates/todo/detail.html`
```html
{% extends "base.html" %}
{% load static %}
{% block content %}

<div class="todoDetail"></div>
<div class="btnList">
    <button class="todoUpdate">수정</button>
    <button class="todoDelete">삭제</button>
</div>

<script>
</script>
{% endblock %}
```

/todo/retrieve/<int:pk>/  특정 Todo 상세 조회
`http://127.0.0.1:8000/todo/api/retrieve/1/`
`TodoRetrieveAPI` `GET`

---
###### 🔹 리스트를 화면에 출력하기

✅ 아래 코드는 `axios`를 사용할 때 공통 설정을 미리 만들어서 계속 반복하지 않도록 도와주는 "axios 인스턴스 생성" 코드입니다.
```JS
const axiosInstance = axios.create({
    baseURL: '/',    // API 베이스 URL
    timeout: 5000,
    headers: { 'Content-Type': 'application/json' }
});
```

| 항목        | 의미            | 예시                                                  |
| --------- | ------------- | --------------------------------------------------- |
| `baseURL` | 기본 요청 주소      | `/`이면 `/todo/api/` → 전체 URL은 `/todo/api/list`처럼 처리됨 |
| `timeout` | 요청 시간 제한 (ms) | `5000` = 5초 안에 응답 없으면 실패로 처리                        |
| `headers` | 요청 헤더         | `Content-Type`은 서버에 JSON 보낸다는 의미                    |
baseURL이란?
`axios`로 요청을 보낼 때 기본이 되는 주소입니다.  
이걸 지정해두면 모든 요청에 자동으로 붙습니다.
```js
const axiosInstance = axios.create({
  baseURL: '/api'
});

axiosInstance.get('/todos');  
// 실제 요청 주소 → "/api/todos"
```
`baseURL`은 URL의 공통 접두사 역할을 합니다.

예시)
```js
baseURL: '/todo/viewsets'

axiosInstance.get('/view/?page=1');
// 실제 요청은 → /todo/viewsets/view/?page=1
```

서버 주소: `http://127.0.0.1:8000`
요청하려는 경로: `/todo/api/list/`

baseURL: `'/'` 설정한 경우
```js
const axiosInstance = axios.create({
  baseURL: '/',  // 루트부터 시작
});
```

```
http://127.0.0.1:8000/ + todo/api/list/ = http://127.0.0.1:8000/todo/api/list/
```
안전하게 항상 루트(/)부터 시작, 현재 페이지 경로에 영향 받지 않음

baseURL을 설정하지 않고 axios 기본 사용한 경우
```
axios.get('todo/api/list/');
```
브라우저에서 실행되는 위치가 중요합니다
예를 들어, 현재 페이지 URL이:
```
http://127.0.0.1:8000/todo/
```
이때 상대경로로 요청하면 실제 요청 주소는:
```
http://127.0.0.1:8000/todo/todo/api/list/
```
경로가 꼬입니다! (404 오류 가능성)이 있습니다.

---
`headers`란?
```js
headers: {
  'Content-Type': 'application/json'
}
```
서버에 요청을 보낼 때, 요청 헤더(Request Header)에 추가되는 메타정보입니다.  
서버가 요청을 어떻게 해석할지를 알려줍니다.
`Content-Type': 'application/json` : 서버에 JSON 형식으로 데이터를 보낸다는 의미

---
✅ 기본 틀 잡기 (HTML + 등록 버튼 이동)
- 목표: 페이지가 열리고 `등록하기 버튼`만 동작하는지 확인
- 테스트: 버튼 클릭 시 `/todo/create/`로 이동되는지만 보면 OK

`1.` HTML 내용이 모두 화면에 나타날 때까지 기다렸다가 `init()` 함수를 실행해요
```js
document.addEventListener('DOMContentLoaded', init);
```
HTML이 먼저 로드되고, JavaScript는 느리게 로드되기 때문에  
`document.addEventListener('DOMContentLoaded', ...)`를 사용하는 겁니다.

---
`2.` 웹페이지가 처음 열릴 때 버튼 클릭 같은 UI 이벤트들을 등록하는 함수(UIEvents)를 실행하는 함수입니다.
```js
function init() {
    UIEvents(); // 1단계: 버튼 등의 UI에 클릭 이벤트 연결
    loadTodoList(); 
    // 2단계: Todo 목록의 페이지네이션 설정에 따라 나뉘는 
    // 첫번째 페이지를 뜻합니다.
}
```
`init()`는 페이지가 열릴 때 실행됩니다.
`init()` 내부에서 `UIEvents()`라는 함수를 호출합니다.

순서대로 해석하면:
`UIEvents();`
버튼 등 HTML 요소에 이벤트(클릭 등)를 연결해주는 함수입니다.

---
`3.` "Todo 등록하기" 버튼에 클릭했을 때 어떤 동작을 할지 연결해요
```js
function UIEvents() {
    document.getElementById('createBtn')
        .addEventListener('click', onCreateClick);
}
```
---
`4.` 버튼을 클릭하면"/todo/create/"주소로 이동해요(Todo 작성 화면으로 이동)
```js
function onCreateClick() {
    window.location.href = '/todo/create/';
}
```
---
✅ Todo 목록 1페이지만 불러오기

`5.` 지정한 페이지 번호의 Todo 목록을 서버에서 받아와서 화면에 보여줘요
```js
function loadTodoList(page) {
    fetchTodoData(page)  // 서버에서 데이터를 받아오고
        .then(data => {

			// 받아온 데이터에서 실제 todo 항목만 꺼내고
            const todos = extractTodoArray(data);
            renderTodoList(todos); // 화면에 출력해요
        })
        
        // 오류가 나면 콘솔에 출력해요
        .catch(err => console.error('리스트 로드 실패:', err));
}
```
---
`6.` axios를 이용해서 해당 페이지의 Todo 데이터를 서버로부터 가져와요
```js
function fetchTodoData(page) {
    return axiosInstance
        .get(`/todo/api/list/?page=${page}`)
        .then(res => res.data);
}  
```
이 코드는 `page` 번호를 쿼리 파라미터로 붙여 특정 페이지 데이터를 요청하는 것입니다.

GenericAPIView + ListModelMixin 또는 `ListAPIView` 기반
```js
.get(`/todo/generics/list/?page=${page}`) //제너릭일때
```

ViewSet + Router 자동 URL 패턴을 사용할 때 나오는 URL입니다.
```js
.get(`/todo/viewsets/view/?page=${page}`) //뷰셋일때
```
---
`7.` 서버에서 받은 JSON 응답의 구조가 다양할 수 있기 때문에,  
그 중에서 실제로 필요한 Todo 목록 배열만 추출하는 역할을 합니다.
```js
function extractTodoArray(data) {
    if (Array.isArray(data.data)) return data.data;
    if (Array.isArray(data.results)) return data.results;
    return []; 
}
```
이 함수의 목적은?
서버에서 받은 응답이 어떤 구조든 간에, 실제 Todo 리스트 배열만 안전하게 꺼내기 위한 유틸 함수입니다.

페이지네이션이 없는 경우 서버응답:
```json
[
  { "id": 1, "name": "공부하기" },
  { "id": 2, "name": "청소하기" }
]
```
이건 단순한 리스트 (`Array`)로 
조건 `Array.isArray(data)`가 `true`가 되므로 바로 `return data;` 실행됨

페이지네이션이 적용된 경우 (DRF 기본 응답 구조) 서버 응답:
```json
{
  "count": 23,
  "next": "/todo/?page=2",
  "previous": null,
  "results": [
    { "id": 1, "name": "공부하기" },
    { "id": 2, "name": "청소하기" }
  ]
}
```
이건 `data.results`가 배열입니다.
조건 `Array.isArray(data.results)`가 `true`가 되므로 `return data.results;` 실행됨

잘못된 응답일 경우:
```json
{
  "error": "잘못된 요청입니다."
}
```
위 조건들을 모두 통과하지 못하면 `return []` → 빈 배열 반환

---
데이터가 들어오는 방식을 확인한다. `[참고]`
APIView (raw list 반환)
```js
function extractTodoArray(data) {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}
```
순수한 `@api_view(['GET'])`나 `APIView` 를 써서 직접 `return Response(my_queryset_list)` 처럼 **리스트 자체**를 그대로 내보내면, 최종 JSON이
```json
[
  { "id": 1, "name": "...", … },
  { "id": 2, "name": "...", … }
]
```
이런 형태로 옵니다. 따라서 `response.data` 가 곧 배열이고, `extractTodoArray` 첫 줄에서 바로 잡아낼 수 있는 거죠.

ViewSet (pagination + 메타데이터 포함)
```js
function extractTodoArray(data) {
  if (Array.isArray(data.data))    return data.data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}
```
`ModelViewSet` 등에서 **페이징(pagination)** 을 사용하도록 설정해 두면, DRF는 기본적으로
```json
{
  "count": 42,
  "next": "http://…?page=2",
  "previous": null,
  "results": [ {…}, {…}, … ]
}
```
와 같이 항목 배열을 감싸는 메타 필드를 같이 붙여줍니다.  
따라서 실제 Todo 객체들은 `data.results`(기본 PageNumberPagination) 또는 여러분이 커스터마이징했다면 `data.data` 같은 다른 키로 옮겨져 있게 되고, 이걸 골라 내려면 두 번째 `extractTodoArray` 형태가 필요합니다.

---
`8.` Todo 목록을 웹페이지에 화면으로 출력해주는 핵심 함수입니다.
```js
function renderTodoList(todos) {
    const container = document.querySelector('.todocontainer');
    container.innerHTML = '';
    todos.forEach(todo => container.appendChild(createTodoElement(todo)));
}
```
이 함수는 `todos` 배열을 받아서,  
HTML `.todocontainer` 요소 안에 있는 기존 내용을 모두 지우고,  
새롭게 할 일 항목들을 하나씩 만들어서 화면에 붙이는 함수입니다.

`const container = document.querySelector('.todocontainer');`
할 일 목록이 표시될 HTML 영역을 선택합니다

`.todocontainer`는 보통 아래와 같이 정의되어 있겠죠:
```html
<div class="todocontainer"></div>
```

`container.innerHTML = '';`
기존에 있던 HTML 내용을 모두 비웁니다 (초기화).
즉, 이전에 표시된 할 일들을 모두 지우고 새로 그릴 준비를 하는 것이죠
왜? → `loadTodoList(page)`로 다시 불러올 때 겹치지 않게!

`todos.forEach(todo => container.appendChild(createTodoElement(todo)));`
`todos`는 서버에서 받아온 할 일 객체들의 배열입니다.
```json
[
  { "id": 1, "name": "공부하기", "complete": false },
  { "id": 2, "name": "운동하기", "complete": true }
]
```
이 배열을 `forEach`로 하나씩 순회하며:
- `createTodoElement(todo)` 함수를 호출해서
- 각각의 할 일 항목을 HTML 요소로 만들고
- `.todocontainer` 안에 `appendChild()`로 추가합니다

---
`9.` 위의 함수와 함께 필수로 사용해야 하는 DOM함수

하나의 Todo 객체를 받아서,  
그 정보를 포함한 HTML 요소를 생성하여 화면에 표시할 수 있도록 반환하는 함수
```js
function createTodoElement(todo) {
    const div = document.createElement('div');
    div.className = 'todo-item';
    div.innerHTML = `
        <p><strong>Name:</strong> ${todo.name}</p>
        <p><strong>Description:</strong> ${todo.description}</p>
        <p><strong>Complete:</strong> ${todo.complete}</p>
        <p><strong>Completed At:</strong> ${datetimeToString(todo.completed_at)}</p>
        <p><strong>Experience Points:</strong> ${todo.exp}</p>
        <button class="completeBtn">완료</button>
        <hr>
    `;
    return div;
```

`const div = document.createElement('div');`
새 `<div>` 요소를 하나 생성합니다.
이 안에 Todo 하나의 정보를 담을 것입니다.

`div.className = 'todo-item';`
생성한 `<div>`에 `class="todo-item"`을 부여합니다.
이 클래스를 이용해 CSS로 스타일을 줄 수 있습니다.
```css
.todo-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
```

`div.innerHTML = `` ; 
`innerHTML`을 사용해 Todo의 내용으로 HTML 구조를 만듭니다.
백틱안에 태그를 만듦니다.

`return div;`
위에서 만든 `<div>` 요소를 반환(return) 하여  
→ 다른 함수(`renderTodoList`)에서 화면에 붙일 수 있도록 합니다.

`datetimeToString(todo.completed_at)`
날짜와 시간을 처럼 사람이 읽기 편한 포맷으로 변환됩니다
```js
// before
"2025-06-19T09:00:00Z"
// after
"2025. 06. 19. 오후 06:00:00"
```

#### 월요일 여기서 부터 시작

---
✅ 완료버튼을 누르면 밑줄 생기게 하기
```js
function createTodoElement(todo) {
	// ....코드생략
  
	// 완료된 항목에는 'completed' 클래스 추가 → 밑줄 적용
	if (todo.complete) {
	 div.classList.add('completed');
	}
```

밑줄생기게 css작성하기
```css
.todo-item.completed {
    text-decoration: line-through;
}
```

---
✅  상세보기 이동 및 완료 처리 버튼
- 목표: 각 항목 클릭 시 상세보기로 이동, `완료` 버튼으로 PATCH 요청
- 테스트: 로그 찍거나 응답 후 리스트 갱신되는지 확인
위의 같은 함수내에 `createTodoElement(todo)`
```js
    // 클릭 시 상세 페이지 이동
    div.addEventListener('click', () => detailView(todo.id));
```
- `div` 요소(각 Todo 아이템)에 클릭 이벤트를 붙입니다.
- 클릭하면 **화살표 함수** (`() => detailView(todo.id)`)가 실행되고,
- `detailView(todo.id)` 내부에서
```js
window.location.href = `/todo/detail/${todo.id}/`;
```
처럼 브라우저를 해당 URL로 이동시켜 주기 때문에
결과적으로 “리스트 항목을 클릭하면 `/todo/detail/<pk>/` 페이지가 열리는” 동작이 됩니다.

Pk Todo의 상세 페이지로 이동
```js
// --- 7. 상세보기 이동 --------------------------
// 특정 Todo의 상세 페이지로 이동
function detailView(id) {
    window.location.href = `/todo/detail/${id}/`;
}
```
---
위의 같은 함수내에 `createTodoElement(todo)`
완료 버튼클릭 이벤트
```js
    // 완료 버튼 클릭 시 완료 API 호출
    div.querySelector('.completeBtn')
        .addEventListener('click', e => {
            e.stopPropagation();
            toComplete(todo.id);
        });
```

HTML 구조가 이렇게 있을 때를 가정해 봅시다:
```html
<a href="https://example.com" id="link">
  <button id="btn">클릭하세요</button>
</a>
```
`#child` 버튼을 누르면
- `#parent`의 캡처링 리스너(있다면)
- `#child`의 클릭 리스너
- `#parent`의 버블링 리스너
- `document` → `window` 순으로  
    전부 실행될 수 있습니다.

```js
document.getElementById('link').addEventListener('click', function () {
  console.log('부모 a 태그 클릭됨');
});

document.getElementById('btn').addEventListener('click', function () {
  console.log('버튼 클릭됨');
});
```

`e.stopPropagation()` 의 역할
```js
childButton.addEventListener('click', e => {
  e.stopPropagation();
  // … child 전용 로직만 실행 …
});
```
이 한 줄을 쓰면, 버블링 3번 단계에서  
`#parent`나 그 위 상위 요소의 클릭 핸들러가 절대 호출되지 않습니다.

`<button class="completeBtn">완료</button>` 이 클릭되면
`div.querySelector('.completeBtn')` css밑줄 로 이동
`toComplete(todo.id);` pk를 호출하여
아래코드와 같이 서버로 접속하고 완료를 전송한다. 성공하면 
```js
function toComplete(id) {
    axiosInstance.patch(`/todo/viewsets/view/${id}/`, { complete: true })
        .then(() => loadTodoList(1))
        .catch(err => console.error('완료 처리 실패:', err));
}
```
`.then(() => loadTodoList(1))` 다시 화면을 그린다.

동작흐름:
```
[완료 버튼 클릭]
   ↓
이벤트 발생: completeBtn 클릭
   ↓
e.stopPropagation() → 부모의 클릭 이벤트(detailView) 막음
   ↓
toComplete(todo.id) 실행
   ↓
서버에 PATCH 요청 (complete: true)
   ↓
성공하면 loadTodoList(1) → 화면 다시 그림
   ↓
완료된 항목은 "밑줄 스타일" 포함해서 렌더링됨 (CSS)
```

밑줄은 CSS로 처리됨
```js
if (todo.complete) {
  div.classList.add('completed');  // ✅ 완료 시 클래스 추가
}
```
---
###### 🔹 update  api_view.py
```python
# todo/api_view.py
# 수정하기
class TodoUpdateAPI(APIView):
    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error":"해당하는 todo가 없습니다."},
        status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error":"해당하는 todo가 없습니다."},
        status=status.HTTP_404_NOT_FOUND)
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
```

의사코드 : `put` 요청
```
사용자가 특정 Todo를 전체 수정하려고 한다면:

1. 우선 데이터베이스에서 전달받은 pk값을 이용해 Todo 객체를 찾는다.

2. 만약 해당하는 Todo가 존재하지 않는다면:
   - "해당하는 todo가 없습니다."라는 메시지와 함께
   - 404 Not Found 상태 코드를 응답으로 보낸다.

3. Todo가 존재한다면:
   - 요청으로 들어온 데이터를 가지고
   - 기존 Todo 객체에 덮어쓸 준비를 한다.

4. 데이터를 검증한다.
   - 데이터가 올바르지 않으면 예외를 발생시켜 자동으로 에러를 응답한다.

5. 검증에 성공하면 데이터를 저장한다.
   - 즉, Todo 객체를 새 데이터로 업데이트한다.

6. 업데이트된 Todo 객체를 다시 직렬화해서
   - 사용자에게 응답 데이터로 보낸다.
```

(`patch` 요청)
```
사용자가 특정 Todo를 일부만 수정하려고 한다면:

1. pk값으로 해당 Todo 객체를 데이터베이스에서 찾는다.

2. 만약 해당하는 Todo가 없다면:
   - "해당하는 todo가 없습니다."라는 에러 메시지를
   - 404 상태 코드와 함께 응답으로 보낸다.

3. Todo가 있다면:
   - 요청으로 들어온 데이터 중 일부만 가지고
   - 기존 Todo 객체에 업데이트할 준비를 한다.

4. 데이터를 검증한다.
   - 문제가 있다면 즉시 오류 응답을 보낸다.

5. 문제가 없다면:
   - 해당 필드들만 업데이트해서 저장한다.

6. 저장된 결과를 다시 직렬화해서
   - 사용자에게 응답으로 보낸다.
```
---

```python
#todo/views.py
# 수정
class TodoUpdateView(UpdateView):
    model = Todo
    fields = ['name', 'description', 'complete', 'exp']
    template_name = "todo/update.html"
    context_object_name = "todo"
    success_url = reverse_lazy('todo_List')
```

의사코드
```
사용자가 기존 Todo 항목을 수정하려고 요청하면 다음과 같이 처리한다:

1. 수정할 Todo 객체는 Todo 모델에서 가져온다.

2. 수정할 수 있는 필드는 다음과 같다:
   - name
   - description
   - complete
   - exp

3. 이 뷰는 HTML 템플릿을 사용해서 폼을 출력한다.
   - 사용할 템플릿 파일은 "todo/update.html"이다.

4. 템플릿 안에서 사용할 객체의 이름은 "todo"로 지정한다.

5. 사용자가 수정 폼을 제출하고 저장에 성공하면:
   - 수정 후 이동할 페이지는 todo_List라는 URL 이름을 가진 페이지이다.
```



---
######  🔹 삭제하기

`todo/api_views.py`
```python
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TodoSerializer
from .models import Todo

# 삭제하기
class TodoDeleteAPI(APIView):
    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({"error":"해당하는 todo가 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )

        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```


```
사용자가 특정 Todo 항목을 삭제하려고 요청하면 다음과 같이 처리한다:

1. 우선 요청에서 전달된 pk 값을 기반으로
   데이터베이스에서 해당 Todo 항목을 찾는다.

2. 만약 해당하는 Todo가 존재하지 않는다면:
   - "해당하는 todo가 없습니다."라는 에러 메시지와 함께
   - 404 Not Found 상태 코드를 응답으로 보낸다.

3. Todo가 존재하면:
   - 해당 Todo 객체를 데이터베이스에서 삭제한다.

4. 삭제가 완료되면:
   - 응답으로 아무 내용 없이
   - 204 No Content 상태 코드를 반환한다.
```

/todo/delete/<int:pk>/  특정 Todo 삭제
`http://127.0.0.1:8000/todo/api/delete/1/`
`TodoDeleteAPI`  `DELETE

---
###### 🔹 create.html 의사코드
```
1. HTML 문서가 모두 로딩되면 init() 함수를 호출한다.

2. init() 함수는 버튼 클릭 이벤트를 연결하는 함수를 실행한다.

3. 버튼의 id가 'todoCreate'인 요소를 찾는다.
   - 만약 해당 버튼이 없다면 함수 종료.
   - 버튼이 있다면 클릭 이벤트가 발생했을 때 onCreateClick() 함수가 실행되도록 연결한다.

4. 사용자가 'todoCreate' 버튼을 클릭하면:
   - gatherFormData() 함수를 통해 입력 필드의 값을 수집한다.
   - 수집된 값들을 payload라는 객체에 담는다.
   - 이 payload를 가지고 createTodo(payload)를 실행한다.

5. gatherFormData() 함수는 다음 값을 수집한다:
   - id="name"인 요소의 값을 읽어 name 키에 저장
   - id="description"인 요소의 값을 읽어 description 키에 저장
   - id="complete"인 체크박스의 체크 여부를 complete 키에 저장
   - id="completed_at"인 입력값이 있으면 날짜를 ISO 문자열로 변환하여 completed_at 키에 저장
   - id="exp"인 값이 비어있으면 0, 아니면 숫자로 변환하여 exp 키에 저장

6. 이렇게 수집된 데이터를 가지고 axiosInstance를 통해
   - '/todo/generics/create/' 주소로 POST 요청을 보낸다.

7. 요청에 성공하면 onCreateSuccess()가 실행된다.
   - 이 함수는 브라우저를 '/todo/list/' 주소로 이동시킨다.

8. 요청에 실패하면 onCreateError()가 실행된다.
   - 콘솔에 에러 메시지를 출력하고, 사용자에게 alert 창을 띄운다.
```

```js
// --- 1. 문서가 완전히 로드되면 초기화 실행 ---
document.addEventListener('DOMContentLoaded', init);


// --- 2. 초기화: 이벤트 바인딩 실행 ----------
function init() {
  bindUIEvents(); // 버튼에 클릭 이벤트 연결
}

// --- 3. UI 이벤트 바인딩: 생성 버튼 클릭 이벤트 연결 -----

/*
클릭, 스크롤, 탭 키 등의 사용자 행동이 발생했을 때 그 행동과 연결된 함수를 실행하도록 연결하는 것" 이게 바로 UI 이벤트 바인딩입니다.
*/

function bindUIEvents() {
  const btn = document.getElementById('todoCreate');
  if (!btn) return;
  btn.addEventListener('click', onCreateClick); // 클릭 시 4번 실행
}

// --- 4. 생성 버튼 클릭 시 실행되는 핸들러 ---------
function onCreateClick() {
  const payload = gatherFormData(); 
 // 5번:폼 데이터 수집 gatherFormData()함수에서 각input 요소의 값을 읽음
 
  createTodo(payload); // 6번: 서버에 데이터 전송
}

// --- 5. 폼 데이터 수집: 입력값을 객체로 변환 ---------
/*
constant = 상수 -> 값을 재할당 불가능, 반드시 초기값 필요
let = 변수 -> 값 재할당 가능, 나중에 할당 가능

파이썬에서는 PI상수라는 강제 규칙이 없습니다. 단지 대문자는 바꾸지 마세요라는 개발자 간의 약속일 뿐입니다.
그러나 자바스크립트에서는 const를 쓰면 값을 다시 할당하면 에러가 납니다.
*/
function gatherFormData() {
  let expVal = document.getElementById('exp').value;
  if (expVal === '') expVal = 0; 
  //expVal이 빈 문자열('')이라면, expVal에 기본값 0을 넣어라.
  
  const completedAtInput = document.getElementById('completed_at').value; 
 //HTML 요소 중에서 id="completed_at"인 input 요소를 찾아서 
 //그 입력값(value)을 가져오겠다는 뜻입니다.

  const completedAt = completedAtInput ? new Date(completedAtInput).toISOString() : null;

  return {
    name:document.getElementById('name').value, 
  // 이 객체 안에 name이라는 키(key) 를 만들고,그 값(value)은 document.getElementById('name').value로 설정해라."

    description:document.getElementById('description').value,
    complete:document.getElementById('complete').checked,
    completed_at: completedAt,
    exp:Number(expVal),
  };
}

// --- 6. API 호출: Todo 생성 요청 ----------
/*
axios.post(url, data)는 해당 URL로 data 객체를 서버에 POST 방식으로 전송하라는 의미입니다.
*/
function createTodo(data) {
  axiosInstance
    .post('/todo/generics/create/', data)
    .then(onCreateSuccess) // 7번: 성공 시 처리
    .catch(onCreateError); // 8번: 실패 시 처리
}

// --- 7. 생성 성공 핸들러: 목록 페이지로 이동 -----
function onCreateSuccess(response) {
  // 생성 후 목록 페이지로 이동
  window.location.href = '/todo/list/';
}

// --- 8. 생성 실패 핸들러: 에러 알림 ----------
function onCreateError(error) {
  console.error('Todo 생성 실패:', error);
  alert('Todo 생성에 실패했습니다.');
}
```

/todo/create/<int:pk>/  특정 Todo 수정
`http://127.0.0.1:8000/todo/api/create/`
`TodoCreateAPI`  `POST`

---
###### 🔹 todo/detail.html 의사코드
```
1. 문서가 완전히 로드되면 init() 함수를 실행하라.

2. init() 함수 내부에서 다음 작업을 차례대로 실행하라:
   - 현재 페이지의 URL 경로에서 Todo의 id(pk)를 추출한다.
   - 이 id를 이용해서 해당 Todo 항목의 상세 데이터를 서버에서 불러온다.
   - 데이터를 받아오면 화면에 Todo 상세 정보를 표시한다.
   - 수정 버튼이 존재한다면, 클릭했을 때 수정 페이지로 이동하도록 이벤트를 연결한다.
   - 삭제 버튼이 존재한다면, 클릭했을 때 삭제 여부를 물어보고, 확인하면 삭제 요청을 보내도록 이벤트를 연결한다.

3. URL 경로에서 Todo의 id(pk)를 추출하라:
   - 현재 브라우저 주소창의 경로(`/todo/detail/3/` 등)를 `/` 기준으로 나눠 배열로 만들고,
   - 비어 있지 않은 값들만 필터링한 후,
   - 그 배열의 마지막 요소를 반환하라 (예: "3").

4. 해당 pk를 이용해서 서버에 GET 요청을 보내 Todo 데이터를 받아오라.
   - 주소는 `/todo/viewsets/view/<pk>/` 형식이다.
   - 응답이 성공하면 renderTodoDetail() 함수로 데이터를 넘겨 화면에 표시하라.
   - 실패하면 콘솔에 오류 메시지를 출력하라.

5. 받은 Todo 데이터를 기반으로 HTML 요소를 동적으로 만들어 `.todoDetail` 영역에 삽입하라:
   - 이름(name), 설명(description), 완료 여부(complete),
     완료 날짜(completed_at), 경험치(exp) 등을 HTML 구조로 보여줘라.

6. 수정 버튼(.todoUpdate)을 찾고, 존재하면 다음 동작을 연결하라:
   - 버튼이 클릭되었을 때, `/todo/update/<pk>/` 주소로 페이지를 이동시켜라.

7. 삭제 버튼(.todoDelete)을 찾고, 존재하면 다음 동작을 연결하라:
   - 버튼 클릭 시 사용자에게 정말 삭제할 것인지 확인을 요청하라.
   - 확인을 받으면 `/todo/generics/delete/<pk>/` 주소로 DELETE 요청을 보내라.
   - 삭제 요청이 성공하면 목록 페이지(`/todo/list/`)로 이동하라.
   - 실패하면 alert 창으로 오류를 알려줘라.
```

`todo > urls.py`
```python
from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # APIView  
    api_views.TodoDeleteAPI.as_view(), name="todo_api_delete"),
]
```

```js
{% extends "base.html" %}
{% load static %}
{% block content %}

<div class="todoDetail"></div>
<div class="btnList">
    <button class="todoUpdate">수정</button>
    <button class="todoDelete">삭제</button>
</div>

<script src="{% static 'js/axios.min.js' %}"></script>
<script>

// --- 공통 Axios 인스턴스 정의 ----------------
// const axiosInstance = axios.create({
//    baseURL: '/',    
//    timeout: 5000,
//    headers: { 'Content-Type': 'application/json' }
// }); 

  
// --- 1. 초기화 -------------------------------
document.addEventListener('DOMContentLoaded', init);

// --- 2.
function init() {
    const pk = getTodoId();
    loadTodoDetail(pk);
    bindUpdateButton(pk);
    bindDeleteButton(pk);
}

// --- 3. URL에서 PK 추출 -----------------------
function getTodoId() {
    // 예: /todo/detail/3/ → ["todo","detail","3"] → pop() → "3"
    return window.location.pathname
               .split('/')
               .filter(Boolean)
               .pop();
}

// --- 4. 상세 정보 로드 & 렌더링 ---------------
function loadTodoDetail(pk) {
    // 수정된 API 경로: TodoRetrieveAPI → /todo/api/retrieve/<pk>/
    axiosInstance
        .get(`/todo/viewsets/view/${pk}/`)      // ← 주소 수정: retrieve endpoint 사용
        .then(res => renderTodoDetail(res.data))
        .catch(err => console.error('상세 조회 실패:', err));
}

// --- 5.
function renderTodoDetail(todo) {
    const container = document.querySelector('.todoDetail');
    container.innerHTML = `
        <div class="todo-item">
            <p><strong>Name:</strong> ${todo.name}</p>
            <p><strong>Description:</strong> ${todo.description}</p>
            <p><strong>Complete:</strong> ${todo.complete}</p>
            <p><strong>Completed At:</strong> ${todo.complete_at}</p>
            <p><strong>Experience Points:</strong> ${todo.exp}</p>
        </div>
    `;
}

// --- 6. 수정 버튼 바인딩 ----------------------
function bindUpdateButton(pk) {
    const btn = document.querySelector('.todoUpdate');
    if (!btn) return;
    btn.addEventListener('click', () => {
        // 수정 페이지 이동 (백엔드 뷰: TodoUpdateAPI는 API용, 프론트엔드 URL은 별도)
        window.location.href = `/todo/update/${pk}/`;
    });
}

// --- 7. 삭제 버튼 바인딩 ----------------------
function bindDeleteButton(pk) {
    const btn = document.querySelector('.todoDelete');
    if (!btn) return;
    btn.addEventListener('click', () => {
        if (!confirm('정말 해당 Todo를 삭제하시겠습니까?')) return;
        // 수정된 API 경로: TodoDeleteAPI → /todo/api/delete/<pk>/
        axiosInstance
            .delete(`/todo/generics/delete/${pk}/`)  // ← 주소 수정: delete endpoint 사용
            .then(() => window.location.href = '/todo/list/')
            .catch(() => alert('Todo 삭제에 실패했습니다.'));
    });
}
</script>
{% endblock %}
```

/todo/detail/<int:pk>/  특정 Todo 수정
`http://127.0.0.1:8000/todo/api/retrieve/<int:pk>`
`TodoRetrieveAPI`  `GET`

---
###### 🔹 todo/update.html 의사코드
```
1. 문서가 완전히 로드되면 init() 함수를 실행한다.

2. init() 함수에서 다음과 같은 초기 작업을 진행한다:
   - 브라우저 주소(URL)에서 pk(할 일의 고유 ID)를 추출한다.
   - 해당 pk를 이용해서 서버에서 기존 Todo 데이터를 불러오고, HTML 폼에 값을 채운다.
   - 수정 버튼이 클릭될 수 있도록 이벤트를 연결한다.

3. getTodoId():
   현재 브라우저 주소 경로(`/todo/update/5/`)에서 마지막 요소("5")를 추출한다.
   이 값을 통해 어떤 Todo를 수정할지 결정한다.

4. loadTodoIntoForm(pk):
   주어진 pk에 해당하는 Todo 데이터를 서버에서 가져오기 위해 GET 요청을 보낸다.
   응답이 성공적으로 오면 populateForm() 함수를 호출해 HTML 폼에 기존 데이터를 채운다.
   요청에 실패하면 콘솔에 에러를 출력한다.

5. populateForm(todo):
   불러온 Todo 데이터를 바탕으로 HTML `<input>` 요소에 값들을 채워 넣는다.
   - 이름(name)과 설명(description)은 `.value`에 넣고,
   - 완료 여부(complete)는 체크박스이므로 `.checked`에 넣는다.
   - 경험치(exp)는 숫자 입력창의 `.value`로 설정한다.

6. bindUpdateButton(pk):
   수정 버튼(`#todoUpdate`)을 찾아서 클릭 이벤트를 연결한다.
   클릭 시 handleUpdate(pk) 함수를 실행하게 만든다.

7. handleUpdate(pk):
   현재 폼에 입력된 값들을 객체(payload)로 수집한다.
   - 이 값들을 JSON 형식으로 PATCH 요청을 보낸다.
   - 주소는 `/todo/generics/update/<pk>/` 형식의 수정 API다.
   - 성공하면 상세보기 페이지(`/todo/detail/<pk>/`)로 이동한다.
   - 실패하면 콘솔에 에러 로그를 출력하고, 사용자에게 실패 alert을 띄운다.

8. redirectToDetail(pk):
   수정이 완료되면 해당 Todo의 상세 페이지(`/todo/detail/<pk>/`)로 브라우저를 이동시킨다.
```

```js
{% extends "base.html" %}
{% load static %}
{% block content %}

<div class="container">
  <h2>Update Your Todo</h2>
  <div>
    <label for="name">Name:</label>
    <input type="text" name="name" id="name">
  </div>

  <div>
    <label for="description">Description:</label>
    <textarea name="description" id="description"></textarea>
  </div>

  <div>
    <label for="complete">Complete:</label>
    <input type="checkbox" name="complete" id="complete">
  </div>

  <div>
    <label for="exp">Experience Points:</label>
    <input type="number" name="exp" id="exp" min="0">
  </div>

  <button type="button" id="todoUpdate">Update</button>
</div>

<script src="{% static 'js/axios.min.js' %}"></script>
<script>


// --- 1. 초기화 -------------------------------
document.addEventListener('DOMContentLoaded', init);

// --- 2. 초기화
function init() {
  const pk = getTodoId();
  loadTodoIntoForm(pk);
  bindUpdateButton(pk);
}

// --- 3. URL에서 PK 추출 ------------------------
function getTodoId() {
  // 예: /todo/update/5/ → ["todo","update","5"] → pop() → "5"
  return window.location.pathname.split('/').filter(Boolean).pop();
}

// --- 4. 기존 Todo 데이터 로드 & 폼 채우기 -----
function loadTodoIntoForm(pk) {
  // 상세조회 API 호출 (TodoRetrieveAPI)
  axiosInstance
    .get(`/todo/generics/retrieve/${pk}/`)            // ← retrieve 엔드포인트
    .then(res => populateForm(res.data))
    .catch(err => console.error('로딩 실패:', err));
}

// --- 5.
function populateForm(todo) {
  document.getElementById('name').value        = todo.name;
  document.getElementById('description').value = todo.description;
  document.getElementById('complete').checked  = todo.complete;
  document.getElementById('exp').value         = todo.exp;
}

// --- 6. 업데이트 버튼 클릭 바인딩 -------------
function bindUpdateButton(pk) {
  const btn = document.getElementById('todoUpdate');
  if (!btn) return;
  btn.addEventListener('click', () => handleUpdate(pk));
}

// --- 7. 업데이트 요청 처리 --------------------
function handleUpdate(pk) {
  const payload = {
    name:        document.getElementById('name').value,
    description: document.getElementById('description').value,
    complete:    document.getElementById('complete').checked,
    exp:         Number(document.getElementById('exp').value),
  };
  // 수정 API 호출 (TodoUpdateAPI)
  axiosInstance
    .patch(`/todo/generics/update/${pk}/`, payload)   
    // ← update 엔드포인트
    
    .then(() => redirectToDetail(pk))
    .catch(err => {
      console.error('수정 실패:', err);
      alert('Todo 수정에 실패했습니다.');
    });
}

// --- 8. 수정 후 상세 페이지로 이동 -------------
function redirectToDetail(pk) {
  window.location.href = `/todo/detail/${pk}/`;
}
</script>
{% endblock %}
```

/todo/update/<int:pk>/  특정 Todo 수정
`http://127.0.0.1:8000/todo/api/update/1/`
`TodoUpdateAPI`  `PATCH` or `PUT`

---
######  탬플릿

`templates/base.html`
```html
{% load static %} 
<!DOCTYPE html>
<html lang="ko">
<head>
  {% include "head.html" %}
</head>
<body>
    {% include 'header.html' %} #추가
	{% block content %}{% endblock %}
	{% include 'footer.html' %} #추가

  <!-- Global Scripts -->
  <script src="{% static 'js/getCookie.js' %}"></script>
  <script src="{% static 'js/axiosInstance.js' %}"></script>
  <script src="{% static 'js/utils.js' %}"></script>

  <!-- 페이지별 개별 스크립트 삽입 위치 -->
  {% block scripts %}{% endblock %}

</body>
</html>
```

`templates/head.html`
```html
{% load static %}
<title>{% block title %}DjangoCourse{% endblock %}</title>

<!-- CSS -->
<link rel="stylesheet" href="{% static 'css/styles.css' %}">

<!-- Axios -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
```

`templates/header.html`
```html
{% load static %}
<div class="header">
  <h1>Todo List</h1>
  <div class="user-actions">
    <a href="{% url 'todo_List' %}" class="nav-link">📋 목록</a>

    {% if user.is_authenticated %}
      <!-- 🔓 로그아웃 버튼 (id 추가) -->
      <button id="logoutBtn" class="nav-link logout">🔓 로그아웃</button>
    {% else %}
      <!-- 🔒 로그인은 여전히 DRF 기본 로그인 뷰 사용 -->
      <a
        href="{% url 'rest_framework:login' %}?next={% url 'todo_List' %}"
        class="nav-link login"
      >🔒 로그인</a>
    {% endif %}
  </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const logoutBtn = document.getElementById("logoutBtn");

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async () => {
      try {
        await axiosInstance.post("/todo/api/custom-logout/");
        window.location.href = "{% url 'todo_List' %}";
      } catch (err) {
        console.error("로그아웃 실패:", err);
        alert("로그아웃 중 오류가 발생했습니다.");
      }
    });
  }
});
</script>
```

`templates/footer.html`
```python
{% load static %}
    <div class = "footer">
      <a href="https://github.com/handgonpo">Contact Me: handgonpo@naver.com</a>
    </div>
```

---
######  utils.js
```js
function datetimeToString(datetime){
    if (!datetime) return "-";
    const date = new Date(datetime);
    return date.toLocaleString("ko-KR", { timeZone: "Asia/Seoul" });
}
```
서버에서 받은 "날짜와 시간 데이터"를  
사람이 읽기 쉬운 한국식 날짜/시간 형식으로 바꿔주는 함수입니다

---



