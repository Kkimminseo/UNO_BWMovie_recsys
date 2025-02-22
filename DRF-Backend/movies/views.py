from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import pandas as pd

from .serializers import SignupMovieListSerializer, GenreSerializer
from accounts.models import User
from .models import GenrePreference, Genre

"""랜덤한 영화 리스트 25개 보여주는 코드"""
@api_view(['GET'])
def SignUpMovieListView(request):
    """이미지 들고올 코드"""
    TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    """csv 불러 오기"""
    df = pd.read_csv(
        '/Users/baeminkyung/Desktop/github/UNO_BWMovie_recsys/dataset/signup_movie_list.csv')
    
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


api_view(['POST'])  # POST 요청만 허용 (장르 선호도 생성)
def CreateGenrePreferenceView(request, user_id):
    """
    CSV에 있는 영화에 속한 장르를 특정 사용자의 GenrePreference DB에 저장.
    1. csv 파일을 읽어온다.
    2. 특정 유저를 가져온다.
    3. csv파일을 순회하며 장르를 가져오고, GenrePreference DB에 저장한다.
    """

    csv_file_path = '/Users/baeminkyung/Desktop/github/UNO_BWMovie_recsys/dataset/signup_movie_list.csv'

    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        return Response({"error": "CSV 파일을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": f"CSV 파일 읽기 오류: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        user = User.objects.get(id=user_id)  # 유저 ID로 유저 가져오기
    except User.DoesNotExist:
        return Response({"error": "해당 ID의 유저를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    try:
        for index, row in df.iterrows():
            genres_str = row['genres']
            if isinstance(genres_str, str):
                genres_list = [s.strip() for s in genres_str.split(',')]

                for genre_name in genres_list:
                    try:
                        # 장르가 존재하는지 확인하고 없으면 생성
                        genre, created = Genre.objects.get_or_create(genre=genre_name)

                        # GenrePreference 생성 ("like"로 설정)
                        genre_preference, created = GenrePreference.objects.get_or_create(
                            user_id_fk=user,
                            genre_id_fk=genre,
                            defaults={'preference_type': 'like'}  # 기본적으로 "like"로 설정
                        )

                        if created:
                            print(f"유저 {user.id}의 {genre_name} 장르 선호도 생성.")
                        else:
                            print(f"유저 {user.id}의 {genre_name} 장르 선호도 이미 존재.")

                    except Exception as e:
                         print(f"장르 선호도 생성 중 오류 발생: {str(e)}") # 에러 발생시 로그 출력
                         continue # 다음 장르로 진행
    except Exception as e:
        return Response({"error": f"GenrePreference 생성 중 오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "장르 선호도 생성이 완료되었습니다."}, status=status.HTTP_201_CREATED)