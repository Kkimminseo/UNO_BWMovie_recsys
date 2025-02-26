"""
TMDB API를 사용하여 최근 개봉 영화 데이터를 수집하는 스크립트

이 스크립트는 TMDB(The Movie Database) API를 사용하여 최근 개봉한 영화들의
정보를 수집하고 CSV 파일로 저장합니다.

Requirements:
    - Python 3.6+
    - requests
    - python-dotenv
    - TMDB API 키 (.env 파일에 TMDB_API_KEY로 설정)
"""

import threading
import requests
import time
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# 상수 정의
OUTPUT_FILE = "recent_movies.csv"  # 출력될 CSV 파일명
DATE_FORMAT = "%Y-%m-%d"  # 날짜 형식
MIN_POPULARITY = 0.6  # TMDB 인기도 최소값
MIN_VOTE_AVERAGE = 4.5  # 평점 최소값 (10점 만점)
DAYS_RANGE = 10  # 수집할 기간 (최근 N일)


# .env 파일에서 API 키 로드
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")


def handle_api_error(func):
    """
    API 호출 관련 예외를 처리하는 데코레이터

    Args:
        func: 데코레이트할 함수

    Returns:
        wrapper 함수
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{func.__name__} 실행 중 에러 발생: {e}")
            return None

    return wrapper


def get_start_date():
    """
    수집 시작 날짜를 계산하여 반환

    Returns:
        str: YYYY-MM-DD 형식의 날짜 문자열
    """
    return (datetime.now() - timedelta(days=DAYS_RANGE)).strftime(DATE_FORMAT)


@handle_api_error
def fetch_page(page):
    """
    TMDB API를 통해 특정 페이지의 영화 목록을 가져옴

    Args:
        page (int): 가져올 페이지 번호

    Returns:
        tuple: (필터링된 영화 목록, 전체 페이지 수)
    """
    url = "https://api.themoviedb.org/3/discover/movie"

    # API 요청 파라미터 설정
    params = {
        "api_key": api_key,
        "sort_by": "primary_release_date.desc",  # 최신순 정렬
        "include_video": "false",  # 비디오 제외
        "page": page,
        "primary_release_date.gte": get_start_date(),  # 시작일 이후
        "vote_average.gte": MIN_VOTE_AVERAGE,  # 최소 평점
        "vote_count.gte": 0,  # 평점이 있는 영화만
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # 인기도 기준으로 필터링
    filtered_results = [
        movie
        for movie in data["results"]
        if movie.get("popularity", 0) >= MIN_POPULARITY
    ]

    return filtered_results, data["total_pages"]


@handle_api_error
def fetch_movie_details(movie_id):
    """
    영화의 상세 정보를 가져옴

    Args:
        movie_id (int): TMDB 영화 ID

    Returns:
        dict: 영화 상세 정보
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key, "append_to_response": "keywords"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # 필요한 필드만 추출하여 반환
    return {
        "id": data.get("id", ""),
        "title": data.get("title", ""),
        "revenue": data.get("revenue", ""),
        "vote_average": data.get("vote_average", ""),
        "imdb_id": data.get("imdb_id", ""),
        "original_title": data.get("original_title", ""),
        "overview": data.get("overview", ""),
        "popularity": data.get("popularity", ""),
        "poster_path": data.get("poster_path", ""),
        "genres": ", ".join([genre["name"] for genre in data.get("genres", [])]),
        "keywords": ", ".join(
            [kw["name"] for kw in data.get("keywords", {}).get("keywords", [])]
        ),
        "release_date": data.get("release_date", ""),
    }


def fetch_recent_movies():
    """
    최근 영화 데이터를 수집

    Returns:
        list: 수집된 영화 정보 목록
    """
    movies = []
    max_workers = 50  # 동시 실행할 최대 스레드 수

    try:
        # 첫 페이지 요청으로 전체 페이지 수 확인
        first_results, total_pages = fetch_page(1)
        if not first_results:
            return movies

        total_pages = min(total_pages, 500)  # API 제한 고려
        print(f"\n=== 최근 {DAYS_RANGE}일 이내 영화 데이터 수집 시작 ===")
        print(f"총 {total_pages}페이지")

        # 병렬 처리를 위한 ThreadPoolExecutor 설정
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            semaphore = threading.Semaphore(10)  # 동시 요청 제한

            def fetch_with_details(page):
                """단일 페이지의 영화 상세 정보를 가져오는 내부 함수"""
                with semaphore:
                    time.sleep(0.01)  # API 요청 간격 조절
                    page_movies, _ = fetch_page(page)
                    if not page_movies:
                        return []

                    detailed_movies = []
                    for movie in page_movies:
                        time.sleep(0.25)  # 상세 정보 요청 간격
                        details = fetch_movie_details(movie["id"])
                        if details:
                            detailed_movies.append(details)
                    return detailed_movies

            # 모든 페이지에 대해 병렬 처리
            futures = {
                executor.submit(fetch_with_details, page): page
                for page in range(1, total_pages + 1)
            }

            # 완료된 작업 처리
            for future in concurrent.futures.as_completed(futures):
                page = futures[future]
                try:
                    page_movies = future.result()
                    movies.extend(page_movies)
                    print(f"페이지 {page}/{total_pages} 완료 (현재 총 {len(movies)}개)")
                except Exception as e:
                    print(f"에러 발생 (페이지: {page}): {e}")

    except Exception as e:
        print(f"데이터 수집 중 에러 발생: {e}")

    return movies


def save_to_csv(movies):
    """
    영화 정보를 CSV 파일로 저장

    Args:
        movies (list): 저장할 영화 정보 목록
    """
    # CSV 파일의 열 정의
    fieldnames = [
        "id",
        "title",
        "revenue",
        "vote_average",
        "imdb_id",
        "original_title",
        "overview",
        "popularity",
        "poster_path",
        "genres",
        "keywords",
        "release_date",
    ]

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for movie in movies:
                writer.writerow({field: movie.get(field, "") for field in fieldnames})
        print(f"{len(movies)}개의 영화 정보가 {OUTPUT_FILE}에 저장되었습니다.")
    except Exception as e:
        print(f"파일 저장 중 에러 발생: {e}")


def main():
    """메인 실행 함수"""
    # 기존 파일이 있다면 삭제
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    start_date = get_start_date()
    print(f"\n=== {start_date} 이후 개봉 영화 데이터 수집 시작 ===")

    movies = fetch_recent_movies()
    print(f"\n총 {len(movies)}개의 영화를 가져왔습니다.")
    save_to_csv(movies)
    print(f"=== 영화 데이터 수집 완료 ===\n")


if __name__ == "__main__":
    main()
