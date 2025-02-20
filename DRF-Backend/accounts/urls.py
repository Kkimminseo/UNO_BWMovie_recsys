from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),  # 회원 가입
    path("login/", views.LogInView.as_view(), name="login"),  # 로그인
    path("logout/", views.LogOutView.as_view(), name="logout"),  # 로그아웃
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 토큰 갱신
]
