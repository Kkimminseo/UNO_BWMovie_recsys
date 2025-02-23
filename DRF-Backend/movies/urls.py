from django.urls import path
from . import views

urlpatterns = [
    path('movielist/', views.SignUpMovieListView.as_view()), # Signup movie list로 가기
    # path('genrepreference/', views.CreateGenrePreferenceView.as_view()), # 선호 장르 생성
    path('moviepreference/', views.CreateMoviePreferenceView.as_view()), # 선호 영화 생성
]
