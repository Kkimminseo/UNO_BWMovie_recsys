from rest_framework import serializers
from .models import Movie

"""df와 drf를 직렬화"""
class SignupMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path']
        read_only_fields = ['id']