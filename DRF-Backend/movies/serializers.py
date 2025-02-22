from rest_framework import serializers
from .models import Movie, Genre

"""GenreSerializer"""
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre']
        
        """따로 수정할 게 아니라면 읽기 모드로 넣어서 데이터 보호"""
        read_only_fields = ['id', 'genre']


"""회원가입 시, 보여지는 영화 포스터 리스트 및 장르"""
class SignupMovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path', 'genres']
        read_only_fields = ['id']