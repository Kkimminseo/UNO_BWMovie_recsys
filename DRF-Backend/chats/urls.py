from django.urls import path
from .views import get_csrf_token, serve_react

urlpatterns = [
    path("csrf-token/", get_csrf_token, name="csrf-token"),
    path("", serve_react, name="react-index"),  # 메인 페이지를 React index.html로 연결
]

