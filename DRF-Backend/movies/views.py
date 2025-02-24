from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
import random

from .models import GenrePreference, MoviePreference, Movie
from .serializers import SignupMovieListSerializer

"""랜덤한 영화 리스트 25개 보여주는 코드"""
class SignUpMovieListView(APIView):

    def get(self, request):
        # 평점 내림차순으로 정렬하고 수익이 3억 달러 이상인 영화 100개 필터링
        top_movies = Movie.objects.filter(revenue__gte=300000000).order_by(
        "-vote_average")[:100]  # 수익이 3억 달러 이상인 영화 중 상위 100개 선택

        # 100개 중 랜덤으로 25개 선택
        random_movies = list(top_movies)  # 쿼리셋을 리스트로 변환
        random_selection = random.sample(
            random_movies, min(25, len(random_movies))
        )  # 랜덤으로 25개 영화 선택

        # 선택된 영화들을 직렬화
        serializer = SignupMovieListSerializer(random_selection, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""선호하는 영화 및 장르 저장하기"""
class CreateMoviePreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated] # 인증된 사용자만

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
        
        """영화 저장이 완료되면 저장된 영화 리스트에서 장르 목록을 추출하여 장르 선호도 데이터베이스에 저장"""
        movies = Movie.objects.filter(pk__in=selected_movie_ids)
        all_genres = {
            genre.strip() for movie in movies for genre in movie.genres.split(",")}

        # 장르 선호도 생성 및 저장
        genre_preferences = [
            GenrePreference(
                user_id_fk=user,
                genre_id=genre_name,
                preference_type="like"
            )
            for genre_name in all_genres
        ]

        GenrePreference.objects.bulk_create(genre_preferences, ignore_conflicts=True)

        return Response(
            {"message": "선호하는 영화가 성공적으로 저장되었습니다."},
            status=status.HTTP_201_CREATED,
        )  # 성공 응답 반환
