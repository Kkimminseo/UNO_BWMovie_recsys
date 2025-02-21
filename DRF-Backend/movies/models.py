from django.db import models
from accounts.models import User
from enum import Enum

"""Enum용 모델"""
class PerformEumsType(Enum):
    like = "like"
    dislike = "dislike"


"""Movie model"""
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB ID(기존 데이터셋의 ID)
    title = models.CharField(max_length=100)  # 제목
    revenue = models.IntegerField(default=0)  # 수익
    vote_average = models.FloatField(default=0.0)  # 평점
    imdb_id = models.CharField(max_length=100, default="")  # IMDB ID
    original_title = models.CharField(max_length=100)  # 원제(개봉국가제목)
    overview = models.TextField(default="")  # 줄거리
    popularity = models.FloatField(default=0.0)  # 인기도
    genres = models.CharField(max_length=100, default="")  # 장르
    poster_path = models.CharField(max_length=100, default="")  # 포스터 경로(url)
    keywords = models.CharField(max_length=100, default="")  # 키워드

    def __str__(self):
        return self.title


"""영화 선호도 정리를 위한 model"""
class MoviePreference(models.Model):
    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE)# FK "유저 ID"
    movie_id_fk = models.ForeignKey(Movie, on_delete=models.CASCADE) # FK "영화 ID"
    preference_type = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in PerformEumsType],
        default=PerformEumsType.dislike.value) #"선호도 유형 (ENUM: like, dislike)"
    # PRIMARY KEY "(user_id_fk, movie_id_fk)"


