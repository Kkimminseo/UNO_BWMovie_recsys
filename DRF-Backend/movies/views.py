from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions, generics
import pandas as pd

from django.conf import settings
from .models import GenrePreference, MoviePreference,Genre, Movie
from .serializers import SignupMovieListSerializer, MoviePreferenceSerializer


"""랜덤한 영화 리스트 25개 보여주는 코드"""
class SignUpMovieListView(generics.ListAPIView):
    serializer_class = SignupMovieListSerializer
    queryset = Movie.objects.all()
    
    # """csv 불러 오기"""
    # def get_queryset(self):
    #     df = pd.read_csv(settings.CSV_FILE_PATH)
    #     sampled_df = df.sample(n=25)[['id', 'original_title', 'poster_path', 'genres']]
        
    #     """
    #     쉼표로 구분된 장르 이름을 Genre 객체 리스트로 변환
    #     """
    #     def get_genres(genres_str):
    #         if isinstance(genres_str, str):
    #             genre_names = [g.strip() for g in genres_str.split(',')]
    #             genres = []
    #             for genre_name in genre_names:
    #                 genre, created = Genre.objects.get_or_create(genre=genre_name)
    #                 genres.append(genre)
    #                 return genres
    #         else:
    #             return []

    #     sampled_df['genres'] = sampled_df['genres'].apply(get_genres)


"""선호하는 영화 저장하기"""
class CreateMoviePreferenceView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated] # 인증된 사용자만
    serializer_class = MoviePreferenceSerializer

    def post(self, request, *args, **kwargs):
        # print(self.__class__.__name__+" post()")
        """
        사용자가 선택한 영화를 받아서, 영화 선호도 데이터베이스에 저장
        """
        # print("request.data : ", request.data)
        selected_movie_ids = request.data.get('movie_id_fk', [])
        # print(type(selected_movie_ids))
        # print("selected_movie_ids: ", selected_movie_ids)
        # 예외 처리: 선택한 영화 개수 제한
        if type(selected_movie_ids) == str:
            selected_movie_ids = [selected_movie_ids]
        # print(type(selected_movie_ids))
        if len(selected_movie_ids) > 5:
            return Response({"error": "선호 영화는 최대 5개까지만 선택할 수 있습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user  # 현재 로그인한 사용자

        # 선호 영화 ID를 순회하며 MoviePreference 객체 생성
        for movie_id in selected_movie_ids:
            # print("movie_id: ", movie_id)
            # print(type(movie_id))
            try:
                movie = Movie.objects.get(id=movie_id)  # 영화 ID로 Movie 객체 조회
                # print("movie: ", movie)
                movie_preference = MoviePreference.objects.create(
                    user_id_fk=user,
                    movie_id_fk=movie,
                    preference_type='like'  # 또는 'dislike' 등, 필요에 따라 변경
                )
                movie_preference.save()
                # print("movie: ", movie)
            except Movie.DoesNotExist:
                return Response({"error": f"ID '{movie_id}'에 해당하는 영화가 존재하지 않습니다."},
                                status=status.HTTP_400_BAD_REQUEST)

                MoviePreference.save()
        return Response({"message": "선호하는 영화가 성공적으로 저장되었습니다."},
                        status=status.HTTP_201_CREATED)  # 성공 응답 반환


# class CreateGenrePreferenceView(APIView):
    # permission_classes = [permissions.IsAuthenticated]  # 로그인된 사람만 접근 가능
    # """
    # 장르 선호도 생성/조회
    # """

    # def get(self, request):
    #     """
    #     특정 사용자의 장르 선호도 목록을 조회
    #     """
    #     user = request.user  # 현재 인증된 사용자
    #     genre_preferences = GenrePreference.objects.filter(user_id_fk=user)
    #     genre_data = [{'genre_id_fk': p.genre_id_fk.id,
    #                    'genre': p.genre_id_fk.genre,
    #                    'preference_type': p.preference_type} for p in genre_preferences]
    #     return Response(genre_data, status=status.HTTP_200_OK)


    # def post(self, request):
    #     """
    #     사용자가 선택한 장르를 받아서 장르 선호도 데이터베이스에 저장
    #     """
    #     # 요청 데이터에서 선택한 장르 목록 가져오기. 없으면 빈 리스트 사용
    #     selected_genres = request.data.get('selected_genres', [])  
    #     user = request.user  # 현재 인증된 사용자 가져오기

    #     for genre_name in selected_genres:
    #         # 장르 이름으로 장르 객체 가져오기
    #         genre = Genre.objects.get(genre=genre_name)  # DB에서 찾
    #         # 장르 선호도 객체 가져오기
    #         GenrePreference.objects.get(
    #             user_id_fk=user, # 사용자 ID
    #             genre_id_fk=genre,  # 장르 ID
    #             defaults={'preference_type': 'like'}  # 기본 설정: '좋아요' (선호)
    #         )
            
            
    #     return Response(status=status.HTTP_201_CREATED)  # 성공적으로 생성되면 201 응답 반환