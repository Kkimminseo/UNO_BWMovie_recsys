from django.urls import path
from . import views

urlpatterns = [
    path('movielist/', views.SignUpMovieListView), # Signup movie list로 가기
    path('genrepreference/<int:genre_id>/', views.CreateGenrePreferenceView) # 선호 장르 생성
]
