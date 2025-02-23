from django.db import models
from accounts.models import User

"""Genres model"""
class Genre(models.Model):
    id = models.AutoField(primary_key=True) # 장르 ID (AutoField)
    genre = models.CharField(max_length=100) # 장르 이름 (CharField)
 
    def __str__(self):
        return self.genre


"""Movie model"""
class Movie(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # TMDB ID(기존 데이터셋의 ID)
    title = models.CharField(max_length=100)  # 제목
    revenue = models.IntegerField(default=0)  # 수익
    vote_average = models.FloatField(default=0.0)  # 평점
    imdb_id = models.CharField(max_length=100, default="")  # IMDB ID
    original_title = models.CharField(max_length=100)  # 원제(개봉국가제목)
    overview = models.TextField(default="")  # 줄거리
    popularity = models.FloatField(default=0.0)  # 인기도
    """genres : CharField에서 ManyToManyField로 변경"""
    genres = models.ManyToManyField(Genre, related_name="movies")  # 장르
    poster_path = models.CharField(max_length=100, default="")  # 포스터 경로(url)
    keywords = models.CharField(max_length=100, default="")  # 키워드

    def __str__(self):
        return self.title


"""영화 선호도 정리를 위한 model"""
class MoviePreference(models.Model):
    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_preference')# FK "유저 ID"
    movie_id_fk = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_preference') # FK "영화 ID"
    preference_type = models.CharField(
        max_length=10,
        choices=[('like', 'Like'), ('dislike', 'Dislike')],
        default='dislike') # 선호도 유형 like, dislike

    """데이터베이스 내에서 고유하도록 강제하여, 복합 primary key rngus"""
    class Meta:
        unique_together = ('user_id_fk', 'movie_id_fk')
        
    def __str__(self):
        return f"{self.user_id_fk} liked/disliked {self.movie_id_fk}."
    

"""장르 선호도 정리를 위한 model"""
class GenrePreference(models.Model):
    user_id_fk = models.ForeignKey(User, on_delete=models.CASCADE) # FK 유저 ID
    genre_id_fk = models.ForeignKey(Genre, on_delete=models.CASCADE) # FK 장르 ID
    preference_type = models.CharField(
        max_length=10,
        choices=[('like', 'Like'), ('dislike', 'Dislike')],
        default='dislike') # 선호도 유형 like, dislike
    
    """데이터베이스 내에서 고유하도록 강제하여, 복합 primary key와 같은 역할을 함"""
    class Meta:
        unique_together = ('user_id_fk', 'genre_id_fk')
        
    def __str__(self):
        return f"{self.user_id_fk} liked/disliked {self.genre_id_fk}."