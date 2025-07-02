
	[feat] django (Day 3)
	-  GenericAPIView
	-  Edit urls.py
	-  Edit apis.py
	-  imsomnia

`todo > urls.py`
``` python
urlpatterns = [
	# APIView

	# GenericAPIView
	path("generics/create/", TodoGenericsCreateAPI.as_view()),
	path("generics/list/", TodoGenericsListAPI.as_view()),
	path("generics/retrieve/<int:pk>/", TodoGenericsRetrieveAPI.as_view()),
	path("generics/update/<int:pk>/", TodoGenericsUpdateAPI.as_view()),
	path("generics/delete/<int:pk>/", TodoGenericsDeleteAPI.as_view()),
]
```
`.post('/todo/generics/create/', data)`
.patch(`/todo/generics/update/${pk}/`, payload)
.get(`/todo/generics/retrieve/${pk}/`)
.delete(`/todo/generics/delete/${pk}/`)
.get(`/todo/generics/retrieve/${pk}/`)
.get(`/todo/generics/list/?page=${page}`)
axiosInstance.patch(`/todo/generics/update/${id}/`

`todo > api_views.py`
``` python
# generics을 위해 모듈추가
from rest_framework import generics
# from rest_framework import status, generics 
# -> 같은 모듈안에 있으므로 합치기

# REST Framework_GenericAPIView        
class TodoGenericsListAPI(generics.ListAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

class TodoGenericsCreateAPI(generics.CreateAPIView):
	serializer_class = TodoSerializer

class TodoGenericsRetrieveAPI(generics.RetrieveAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer
  
class TodoGenericsUpdateAPI(generics.UpdateAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

class TodoGenericsDeleteAPI(generics.DestroyAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

# Generics list + create
class TodoGenericsListCreateAPI(generics.ListCreateAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

# Generics retriver + update + delete
class TodoGenericsRetrieveUpdateDeleteAPI
(generics.RetrieveUpdateDestroyAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer
```
axiosInstance.patch(`/todo/viewsets/view/${id}/`
.get(`/todo/viewsets/view/${pk}/`)

---
로그인 로그아웃
직접 로그인/회원가입/로그아웃 화면을 만들고 싶다면?
- `/api-auth/login/` 대신, 자신만의 로그인 폼을 만들고
- DRF에서 토큰 기반(JWT 등) 로그인 API를 만들거나
- Session 기반 로그인 처리를 위한 `LoginView`, `LogoutView`를 따로 구성해야 합니다.

```python
# config/urls.py
path('api-auth/', include('rest_framework.urls')),
```

```python
# config/settings.py
LOGIN_REDIRECT_URL = '/todo/list/'
```

단순한 로그아웃 → Django 기본 `logout()` 함수 + URL 연결만으로 충분합니다.
header.html 
```html
{% load static %}
<div>
    <h1> Todo List</h1>
    <div>
      <a href="{% url 'todo_List' %}">목록</a>
      {% if user.is_authenticated%}
        <button><a href="{% url 'custom-logout' %}">로그아웃</a></button>
      {%else%}  
        <a href="{% url 'rest_framework:login' %}?next={% url 'todo_List'%}">로그인</a>
      {%endif%}
    </div>
</div>
```

---

단순구조방식
```python
# todo/urls.py
# ViewSet
path("api/custom-logout/", api_views.CustomLogoutAPI.as_view(), name="custom_logout"),
```

```python
# todo/api_views.py
from django.contrib.auth import logout

class CustomLogoutAPI(APIView):
    def get(self, request):  
        logout(request)
        # return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        return redirect('todo_List')
```

---

**Vue/React SPA**처럼 REST API 중심 구조라면 `axios` 방식으로 처리해야 합니다.
```html
// templates/header.html

{% load static %}
<div class="header">
  <h1>Todo List</h1>
  <div class="user-actions">
    <a href="{% url 'todo_List' %}" class="nav-link">📋 목록</a>

    {% if user.is_authenticated %}
      <!-- 🔓 로그아웃 버튼 (id 추가) -->
      {% comment %} <button><a href="{% url 'custom-logout' %}">로그아웃</a></button>  {% endcomment %}
        <button id="logoutBtn">로그아웃</button>
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
  document.getElementById("logoutBtn").addEventListener("click", () => {
    axiosInstance.get("/todo/api/custom-logout/")
      .then(() => {
        window.location.href = "{% url 'todo_List' %}";
      })
      .catch(err => {
        console.error("로그아웃 실패:", err);
        alert("로그아웃 중 오류가 발생했습니다.");
      });
  });
});
</script>
```

실제로 언제 어떤 걸 써야 하나요?
- 단순한 로그아웃 → Django 기본 `logout()` 함수 + URL 연결만으로 충분합니다.
- axios로 로그아웃을 처리하려면 `CustomLogoutAPI` 같은 POST용 API 뷰를 추가로 만들어야 하며, 자바스크립트에서 호출해야 합니다.

> 만약 템플릿 기반 + 세션 로그인이라면, 굳이 복잡하게 `axiosInstance.post()`를 만들 필요는 없습니다.  
> 반대로 Vue/React SPA처럼 REST API 중심 구조라면 `axios` 방식이 더 자연스럽습니다.