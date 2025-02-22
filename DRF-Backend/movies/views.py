from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import pandas as pd

from django.conf import settings
from .models import GenrePreference, Genre
from .serializers import SignupMovieListSerializer


"""랜덤한 영화 리스트 25개 보여주는 코드"""
class SignUpMovieListView(APIView):
    def get(self, request):
        """csv 불러 오기"""
        df = pd.read_csv(settings.CSV_FILE_PATH)

        """이미지 들고올 코드"""
        TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

        """100개의 original_title, poster_path 열 중에서 25개 랜덤으로 데리고 옴"""
        sampled_df = df.sample(n=25)[['original_title', 'poster_path', 'genres']]

        """poster_path를 완전한 이미지 URL로 변환"""
        sampled_df['poster_url'] = TMDB_IMAGE_BASE_URL + sampled_df['poster_path']

        data = sampled_df[['original_title', 'genres']].to_dict(orient='records')

        """serializer를 사용하여 데이터 변환 및 유효성 검사"""
        serializer = SignupMovieListSerializer(data=data, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGenrePreferenceView(APIView):
    """
    장르 선호도 생성/조회
    """

    def get(self, request):
        """
        특정 사용자의 장르 선호도 목록을 조회
        """
        user = request.user  # 현재 인증된 사용자
        genre_preferences = GenrePreference.objects.filter(user_id_fk=user)
        genre_data = [{'genre_id_fk': p.genre_id_fk.id,
                       'genre': p.genre_id_fk.genre,
                       'preference_type': p.preference_type} for p in genre_preferences]
        return Response(genre_data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        사용자가 선택한 장르를 받아서 장르 선호도 데이터베이스에 저장
        """
        # 요청 데이터에서 선택한 장르 목록 가져오기. 없으면 빈 리스트 사용
        selected_genres = request.data.get('selected_genres', [])  
        user = request.user  # 현재 인증된 사용자 가져오기

        for genre_name in selected_genres:
            # 장르 이름으로 장르 객체 가져오기
            genre = Genre.objects.get(genre=genre_name)  # DB에서 찾
            # 장르 선호도 객체 가져오기
            GenrePreference.objects.get(
                user_id_fk=user, # 사용자 ID
                genre_id_fk=genre,  # 장르 ID
                defaults={'preference_type': 'like'}  # 기본 설정: '좋아요' (선호)
            )
        return Response(status=status.HTTP_201_CREATED)  # 성공적으로 생성되면 201 응답 반환