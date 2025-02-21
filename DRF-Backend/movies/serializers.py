from rest_framework import serializers
from .models import MoviePreference

"""df와 drf를 직렬화"""
class SignupMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviePreference
        fields = ['id', 'original_title', 'poster_path']
        read_only_fields = ['id']