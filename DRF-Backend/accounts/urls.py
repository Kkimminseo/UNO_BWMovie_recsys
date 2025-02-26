from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"), # 회원 가입
    path('login/', views.LogInView.as_view(), name="login"), # 로그인
    path('logout/', views.LogOutView.as_view(), name="logout"), # 로그아웃
    path("csrf-token/", views.get_csrf_token, name="csrf-token"),
]
