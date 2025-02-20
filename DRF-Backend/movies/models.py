from django.db import models


# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB ID(기존 데이터셋의 ID)
    title = models.CharField(max_length=100)  # 제목
    revenue = models.IntegerField  # 수익
    vote_average = models.IntegerField  # 평점
    imdb_id = models.CharField(max_length=100)  # IMDB ID"
    original_title = models.CharField(max_length=100)  # 원제(개봉국가제목)
    overview = models.TextField  # 줄거리
    popularity = models.IntegerField  # 인기도
    genres = models.CharField(max_length=100)  # 장르
    poster_path = models.CharField(max_length=100)  # 포스터 경로(url)
    keywords = models.CharField(max_length=100)  # 키워드

    def __str__(self):
        return self.title
