from rest_framework import serializers
from .models import Movie, Genre, MoviePreference

"""GenreSerializer"""
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre']
        
        """따로 수정할 게 아니라면 읽기 모드로 넣어서 데이터 보호"""
        read_only_fields = ['id', 'genre']


"""MovieSerializer"""
class MoviePreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviePreference
        fields = ['movie_id_fk', 'perference_type']
        
    def create(self, validated_data):
        # 현재 사용자 데려오기
        user = self.context['request'].user
        movie = validated_data['movie_id_fk']
        # 기본값으로 like 설정
        preference_type = validated_data.get('preference_type', 'like')
        
        # 선호 영화 선택 시, body에 입력할 list
        movie_preference, created = MoviePreference.objects.get_or_create(
            user_id_fk=user,
            movie_id_fk=movie,
            defaults={'preference_type': preference_type}
        )
        # 만약 생성되지 않았다면, 위에 정의한 moive_preference 값을 넣고 저장
        if not created:
            movie_preference.preference_type = preference_type
            movie_preference.save()
        return movie_preference


"""회원가입 시, 보여지는 영화 포스터 리스트 및 장르"""
class SignupMovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'original_title', 'poster_path', 'genres']
        read_only_fields = ['id']