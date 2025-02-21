from django.urls import path
from . import views

urlpatterns = [
    path('movielist/', views.SignUpMovieListView), # Signup movie list로 가기
]
