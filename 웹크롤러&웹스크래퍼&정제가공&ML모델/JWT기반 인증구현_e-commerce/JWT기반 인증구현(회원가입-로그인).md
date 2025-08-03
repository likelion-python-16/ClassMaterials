```bash
mkdir e-commerce
cd e-commerce

python -m venv .venv
source .venv/bin/activate
pip install django djangorestframework gunicorn python-dotenv
pip install djangorestframework-simplejwt
pip install requests

django-admin startproject proj .
python manage.py startapp users
python manage.py startapp payments

# 패키지 기록
pip freeze > requirements.txt
```

디렉토리 구조
```
e-commerce/                   # 프로젝트 루트 (이름 예시)
├── .env                      # 환경 변수: TOSS_CLIENT_KEY, TOSS_SECRET_KEY 등
├── requirements.txt          # 필요한 패키지 목록
├── manage.py                 # Django 진입점
├── db.sqlite3                # (예: 개발용 DB)
├── proj/              # 프로젝트 설정 모듈
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py    # JWT-only, static, .env 로딩 등 설정
│   ├── urls.py        # 루트 URLconf (include payments.urls)
│   └── wsgi.py
├── payments/          # 앱 (회원가입/로그인/결제)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py   # RegisterSerializer 등
│   ├── views.py # RegisterView, VerifyPaymentView, 페이지 렌더링 등
│   ├── urls.py  # /api/register/, /api/token/, /payment-page/ 등
│   ├── tests.py
│   ├── static/  # 앱별 static (선택적, collectstatic 시 병합됨)
│   │   └── css/
│   │       └── styles.css    # 공통 스타일
│   └── templates/           # 템플릿
│       ├── register.html
│       ├── login.html
│       ├── payment_page.html
│       ├── success.html
│       └── fail.html
└── venv/ (또는 venv 심볼릭)   # 가상환경 (버전 관리 제외)
```

settings.py
```python
# 환경변수 로드 (SECRET KEY 등 사용)
import os
from dotenv import load_dotenv
load_dotenv()

# 추가된 앱 및 프레임웍
INSTALLED_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "payments",
    "users",
]

TEMPLATES = [
    {
        "DIRS": [BASE_DIR / "payments" / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
"django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 정적파일
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# DRF 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
  "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY")
TOSS_CLIENT_KEY = os.getenv("TOSS_CLIENT_KEY")
```

URL 및 앱 설정
`proj/urls.py` 구성:
```python
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("payments.urls")),  # /payment-page/, /toss/success/ 등
    path("", RedirectView.as_view(url="/payment-page/", permanent=False)),  # 루트 → 결제 페이지
]
```
---

회원가입/로그인 (JWT)
`users/serializers.py`
```python
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
```

users/views.py
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공!"}, status=201)
        return Response(serializer.errors, status=400)
```

users/urls.py
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),      # 회원가입
    path("token/", TokenObtainPairView.as_view()),  # 로그인(JWT)
]
```
---

Toss 결제 HTML 템플릿 준비
`payments/templates/payment_page.html` 생성:
```python
{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>결제</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="{% static 'css/styles.css' %}" />
</head>
<body>
  <div class="card" style="max-width:720px;margin:2rem auto;">
    <h1>결제하기</h1>
    <div id="user-info" style="margin-bottom:10px;"></div>

    <div id="payment-messages"></div>
    <form id="payment-form">
      <label>고객 이름 <input type="text" id="customer-name" required /></label><br>
      <label>주문명 <input type="text" id="order-name" required /></label><br>
      <label>금액(원) <input type="number" id="amount" required min="100" /></label><br>
      <label><input type="checkbox" id="agree" /> 이용약관 동의</label><br>
      <button type="submit">결제하기</button>
    </form>
    <p>로그아웃: <button onclick="logout()">로그아웃</button></p>
  </div>

  <script src="https://js.tosspayments.com/v1"></script>
  <script>
    const clientKey = "{{ toss_client_key }}";
    const tossPayments = TossPayments(clientKey);

    function showMessage(msg, type="error") {
      const container = document.getElementById("payment-messages");
      container.innerHTML = `<div style="padding:10px;border-radius:6px;background:${type==='error'?'#ffe6e6':'#e6ffed'};color:${type==='error'?'#a33':'#166f3c'};">${msg}</div>`;
    }

    function logout() {
      localStorage.removeItem("access_token");
      window.location.reload();
    }

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("로그인 먼저 해주세요.");
      window.location.href = "/login/";
    } else {
      // 사용자명 보여주기
      fetch("/api/me/", {
        headers: {
          "Authorization": "Bearer " + token
        }
      }).then(r => r.json()).then(user => {
        document.getElementById("user-info").innerText = `로그인된 사용자: ${user.username}`;
      });
    }

    document.getElementById("payment-form").addEventListener("submit", function(e){
      e.preventDefault();
      const orderId = "order_" + Date.now();
      const orderName = document.getElementById("order-name").value.trim();
      const customerName = document.getElementById("customer-name").value.trim();
      const amount = Number(document.getElementById("amount").value);
      const agree = document.getElementById("agree").checked;

      if (!agree) {
        showMessage("약관에 동의해주세요.", "error");
        return;
      }
      if (!orderName || !customerName || isNaN(amount) || amount < 100) {
        showMessage("입력을 정확히 해주세요.", "error");
        return;
      }

      tossPayments.requestPayment("카드", {
        amount,
        orderId,
        orderName,
        customerName,
        successUrl: window.location.origin + "/toss/success/",
        failUrl: window.location.origin + "/toss/fail/"
      });
    });
  </script>
</body>
</html>
```

`payments/templates/login.html`
```html
{% comment %} <!DOCTYPE html>
<html>
<head>
  <title>로그인</title>
</head>
<body>
  <h2>로그인</h2>
  <form id="login-form">
    <label>Username: <input type="text" id="username" /></label><br>
    <label>Password: <input type="password" id="password" /></label><br>
    <button type="submit">로그인</button>
  </form>

  <script>
  // 1. 로그인
  document.getElementById("login-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    console.log("✅ 로그인 응답:", result);

    if (result.access) {
      localStorage.setItem("access_token", result.access);
      alert("로그인 성공!");
      location.reload();
    } else {
      alert("로그인 실패");
      console.log(result);
    }
  });

  // 2. 회원가입
  document.getElementById("register-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch("/api/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    if (response.ok) {
      alert("회원가입 성공! 로그인 해주세요.");
      document.getElementById("login-username").value = username;
      document.getElementById("login-password").value = password;
    } else {
      alert("회원가입 실패");
      console.log(await response.json());
    }
  });

  // 3. 결제 요청
  document.getElementById("payment-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const token = localStorage.getItem("access_token");
    const orderId = "order_" + Date.now();
    const orderName = document.getElementById("order-name").value;
    const customerName = document.getElementById("customer-name").value;
    const amount = Number(document.getElementById("amount").value);

    const response = await fetch("/toss/request/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      },
      body: JSON.stringify({ orderId, amount, orderName })
    });

    const result = await response.json();
    console.log("결제 응답:", result);

    const toss = TossPayments("test_ck_클라이언트키");

    if (result.nextRedirectUrl) {
      toss.requestPayment("카드", {
        amount,
        orderId,
        orderName,
        customerName,
        successUrl: "http://localhost:8000/toss/success/",
        failUrl: "http://localhost:8000/toss/fail/"
      });
    } else {
      alert("결제 요청 실패");
      console.log(result);
    }
  });

  // 4. 토큰 존재 시 로그인 생략
  const access = localStorage.getItem("access_token");
  if (access) {
    document.getElementById("auth-forms").style.display = "none";
    document.getElementById("payment-section").style.display = "block";
  }

  function logout() {
    localStorage.removeItem("access_token");
    alert("로그아웃 완료");
    location.reload();
  }
</script>

</body>
</html> {% endcomment %}


<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>로그인</title>
  <link rel="stylesheet" href="/static/css/styles.css" />
</head>
<body>
  <div class="card" style="max-width:480px;margin:3rem auto;">
    <h2>로그인</h2>
    <div id="message"></div>
    <form id="login-form">
      <label>Username
        <input type="text" id="username" required />
      </label><br>
      <label>Password
        <input type="password" id="password" required />
      </label><br>
      <button type="submit">로그인</button>
    </form>
    <p>계정이 없나요? <a href="/register/">회원가입</a></p>
  </div>

  <script>
    function showMessage(msg, error=true) {
      const el = document.getElementById("message");
      el.innerHTML = `<div style="padding:10px;border-radius:6px;background:${error?'#ffe6e6':'#e6ffed'};color:${error?'#a33':'#166f3c'};">${msg}</div>`;
    }

    document.getElementById("login-form").addEventListener("submit", async function(e){
      e.preventDefault();
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value;

      try {
        const res = await fetch("/api/token/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (data.access) {
          localStorage.setItem("access_token", data.access);
          showMessage("로그인 성공!", false);
          setTimeout(() => window.location.href = "/payment-page/", 400);
        } else {
          showMessage("로그인 실패: 자격 증명 확인");
          console.log(data);
        }
      } catch (err) {
        showMessage("네트워크 오류");
        console.error(err);
      }
    });
  </script>
</body>
</html>
```

`payments/templates/register.html`
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>회원가입</title>
  <link rel="stylesheet" href="/static/css/styles.css" />
</head>
<body>
  <div class="card" style="max-width:480px;margin:3rem auto;">
    <h2>회원가입</h2>
    <div id="message"></div>
    <form id="register-form">
      <label>Username
        <input type="text" id="username" required />
      </label><br>
      <label>Password
        <input type="password" id="password" required />
      </label><br>
      <button type="submit">가입하기</button>
    </form>
    <p>이미 계정이 있나요? <a href="/login/">로그인</a></p>
  </div>

  <script>
    function showMessage(msg, error=true) {
      const el = document.getElementById("message");
      el.innerHTML = `<div style="padding:10px;border-radius:6px;background:${error?'#ffe6e6':'#e6ffed'};color:${error?'#a33':'#166f3c'};">${msg}</div>`;
    }

    document.getElementById("register-form").addEventListener("submit", async function(e){
      e.preventDefault();
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value;

      if (!username || !password) {
        showMessage("아이디와 비밀번호를 모두 입력하세요.");
        return;
      }

      try {
        const res = await fetch("/api/register/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
          showMessage("회원가입 성공! 로그인 페이지로 이동합니다.", false);
          setTimeout(() => window.location.href = "/login/", 800);
        } else {
          showMessage(data.detail || JSON.stringify(data));
        }
      } catch (err) {
        showMessage("네트워크 오류");
        console.error(err);
      }
    });
  </script>
</body>
</html>
```

`payments/templates/success.html`
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>결제 성공</title>
  <link rel="stylesheet" href="/static/css/styles.css" />
</head>
<body>
  <div class="card" style="max-width:600px;margin:3rem auto;">
    <h2>결제 성공</h2>
    <div id="result">검증 중...</div>
  </div>

  <script>
  function getParam(name) {
    const u = new URL(window.location.href);
    return u.searchParams.get(name);
  }

  const paymentKey = getParam("paymentKey");
  const token = localStorage.getItem("access_token");
  const resultEl = document.getElementById("result");

  if (!paymentKey) {
    resultEl.innerText = "paymentKey가 없습니다.";
  } else if (!token) {
    resultEl.innerText = "로그인 필요합니다.";
  } else {
    let attempts = 0;
    const maxAttempts = 10;
    const delay = 1000;

    const poll = async () => {
      attempts += 1;
      resultEl.innerHTML = `<div style="padding:12px;border-radius:6px;background:#fff8e1;color:#555;">결제 처리 중입니다... (${attempts}/${maxAttempts})</div>`;

      try {
        const res = await fetch("/api/verify-payment/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
          },
          body: JSON.stringify({ paymentKey })
        });
        const data = await res.json();

        if (data.status === "DONE") {
          resultEl.innerHTML = `<div style="background:#e6ffed;padding:15px;border-radius:6px;color:#166f3c;">
            ✅ 결제 완료되었습니다. 감사합니다.</div>`;
          return;
        }

        if (attempts < maxAttempts) {
          setTimeout(poll, delay);
        } else {
          // 마지막에도 완료 안 됐으면 안내
          let msg = "결제가 아직 완료되지 않았습니다. 잠시 후 다시 확인하거나 고객센터에 문의하세요.";
          // 결제 계속하기 링크 있으면 보여줌 (optional)
          resultEl.innerHTML = `<div style="background:#ffe6e6;padding:15px;border-radius:6px;color:#a33;">
            ❗ ${msg}
          </div>`;
        }
      } catch (err) {
        resultEl.innerHTML = `<div style="background:#ffe6e6;padding:15px;border-radius:6px;color:#a33;">
          네트워크 오류가 발생했습니다. 페이지를 새로고침해 주세요.
        </div>`;
        console.error(err);
      }
    };

    poll();
  }
</script>

</body>
</html>
```

`payments/templates/fail.html`
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>결제 실패</title>
  <link rel="stylesheet" href="/static/css/styles.css" />
</head>
<body>
  <div class="container" style="max-width:480px; margin:2rem auto;">
    <div class="card">
      <h2>결제 실패</h2>
      <p>결제 과정에서 오류가 발생했습니다. 다시 시도해주세요.</p>
      <p><a href="/payment-page/" class="link">결제 페이지로 돌아가기</a></p>
    </div>
  </div>
</body>
</html>
```

`payments/templates/serializers.py`
```python
from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        # Django가 제공하는 create_user를 쓰면 비밀번호 해싱까지 처리됨
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
```

`payments/templates/views.py`
```python
import base64
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from .serializers import RegisterSerializer

# Register API (JWT not required)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# User detail (for showing username)
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModelSerializer  # 간단히 아래 override

    def get(self, request):
        return Response({"username": request.user.username})

# HTML pages
def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")

def payment_page(request):
    return render(request, "payment_page.html", context={"toss_client_key": settings.TOSS_CLIENT_KEY})

def success_page(request):
    return render(request, "success.html")

def fail_page(request):
    return render(request, "fail.html")

# Verify payment via Toss (requires JWT)
class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        payment_key = request.data.get("paymentKey")
        if not payment_key:
            return Response({"detail": "paymentKey required"}, status=400)

        secret_key = settings.TOSS_SECRET_KEY
        if not secret_key:
            return Response({"detail": "TOSS_SECRET_KEY not configured"}, status=500)

        encoded = base64.b64encode(f"{secret_key}:".encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

        resp = requests.get(f"https://api.tosspayments.com/v1/payments/{payment_key}", headers=headers)
        data = resp.json()

        if resp.status_code != 200:
            return Response({"detail": "Toss lookup failed", "status": "ERROR"}, status=200)

        status_ = data.get("status")
        if status_ == "DONE":
            return Response({"detail": "검증 성공", "status": status_})
        else:
            # IN_PROGRESS 등도 200으로 내려줘서 클라이언트가 계속 폴링함
            return Response({"detail": "결제 진행 중", "status": status_})
```

`payments/templates/urls.py`
```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

urlpatterns = [
    # === API ===
    path("api/register/", views.RegisterView.as_view(), name="api-register"),  # 실제 POST 회원가입
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/me/", views.UserDetailView.as_view(), name="user-detail"),
    path("api/verify-payment/", views.VerifyPaymentView.as_view(), name="verify-payment"),

    # === HTML 페이지 ===
    path("register/", views.register_page, name="register-page"),       # GET /register/ -> HTML
    path("login/", views.login_page, name="login-page"),                # GET /login/ -> HTML
    path("payment-page/", views.payment_page, name="payment-page"),
    path("toss/success/", views.success_page, name="toss-success"),
    path("toss/fail/", views.fail_page, name="toss-fail"),
]
```

실행 및 테스트: 마이그레이션 및 서버 실행
```python
python manage.py migrate
python manage.py runserver
```


Toss 테스트 연동 (연습 전용)
https://developers.tosspayments.com/1339616/accounts/1785330/phases/test/api-keys
![[Pasted image 20250801124003.png]]

###### 확인정보
| 항목                          | 설명                                | 사용 위치                         |
| --------------------------- | --------------------------------- | ----------------------------- |
| **클라이언트 키** (`test_ck_...`) | **프론트엔드 JavaScript에서 사용**         | `TossPayments("test_ck_...")` |
| **시크릿 키** (`test_sk_...`)   | **백엔드(Python, Django 등) 서버에서 사용** | API 인증 헤더에 사용                 |
| **보안 키**                    | 백엔드 내부 검증용 (잘 모르겠으면 생략해도 됨)       | 필요 시 추가 검증용                   |

access_token이 정상적으로 localStorage에 저장되어 있는지 확인하기 위해 
F12 개발자툴에서 크롬 콘솔을 열고 다음을 직접 입력하여 확인합니다.
```consol
localStorage.getItem("access_token")
```

![[Pasted image 20250801114036.png]]