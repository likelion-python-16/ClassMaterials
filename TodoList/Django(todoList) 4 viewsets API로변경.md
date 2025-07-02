
	[feat] django (Day 4)
	-  Viewsets
	-  Edit urls.py
	-  Edit apis.py
	-  imsomnia

`todo > urls.py  viewsets 추가`
```python
# viewset을 위한 모듈 호출
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register("view", TodoViewSet)

 # Viewsets
 path("viewsets/", include(router.urls)), 
 # 127.0.0.1:8000/todo/viewsets/view/
```

`todo > api_views.py  viewsets 추가`
```python
# Viewsets을 위한 모듈추가
from rest_framework import viewsets
# from rest_framework import status, generics viewsets -> 
# 같은 모듈안에 있으므로 합치기

# REST Framework_ViewSets  
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer
```

💡 예시 전체 주소
목록 조회: `http://127.0.0.1:8000/todo/viewsets/view/`
상세 조회: `http://127.0.0.1:8000/todo/viewsets/view/3/` (예: id=3)

|URL|HTTP 메서드|설명|
|---|---|---|
|`/todo/viewsets/view/`|`GET`|Todo 전체 목록 조회 (list)|
|`/todo/viewsets/view/<pk>/`|`GET`|특정 Todo 상세 조회 (retrieve)|
|`/todo/viewsets/view/`|`POST`|새 Todo 생성 (create)|
|`/todo/viewsets/view/<pk>/`|`PATCH`|특정 Todo 수정 (partial_update)|
|`/todo/viewsets/view/<pk>/`|`DELETE`|특정 Todo 삭제 (destroy)|
