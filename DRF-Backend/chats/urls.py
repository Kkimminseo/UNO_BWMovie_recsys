from django.urls import path
from .views import serve_react

urlpatterns = [
    path("", serve_react, name="react-index"),  # 메인 페이지를 React index.html로 연결
]
