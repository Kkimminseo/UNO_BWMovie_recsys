from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd

from django.conf import settings
from .serializers import SignupMovieListSerializer, GenreSerializer
from accounts.models import User
from .models import GenrePreference, Genre

"""랜덤한 영화 리스트 25개 보여주는 코드"""
@api_view(['GET'])
def SignUpMovieListView(request):
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
    return Response(serializer.errors, status=400) # 에러 처리


api_view(['GET'])
def CreateGenrePreferenceView(request, user_id_fk):
    pass