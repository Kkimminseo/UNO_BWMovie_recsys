from django.urls import path
from . import views

urlpatterns = [
    path('api/movielist/', views.SignUpMovieListView.as_view()), # Signup movie list로 가기
]
