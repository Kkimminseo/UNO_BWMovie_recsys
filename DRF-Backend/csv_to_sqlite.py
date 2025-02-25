"""
이 스크립트를 실행하기 전에 다음 단계를 따라주세요:

1. Python 가상환경 생성 및 활성화:
   - Windows:
     python -m venv .venv
     .venv\Scripts\activate
   - Mac/Linux:
     python3 -m venv .venv
     source .venv/bin/activate

2. 필요한 패키지 설치:
   프로젝트 루트의 DRF-Backend 디렉토리에서:
   pip install -r requirements.txt

3. 데이터 파일 준비:
   - 프로젝트 루트에 'dataset' 폴더 생성
   - 'dataset' 폴더에 'recent_movies.csv' 파일 위치

4. 데이터베이스 마이그레이션:
    python manage.py migrate

5. 스크립트 실행:
   python -m csv_to_sqlite
"""

import os
import sys
from tqdm import tqdm

# 프로젝트 루트를 sys.path에 추가하여 import 문제를 방지합니다.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Django 설정 모듈을 지정합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django

django.setup()

from movies.models import Movie

import csv
from datetime import datetime


def import_movies(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            created_count = 0
            updated_count = 0
            skipped_count = 0

            # 전체 행 수를 먼저 계산
            total_rows = sum(
                1 for _ in csv.DictReader(open(file_path, "r", encoding="utf-8"))
            )
            file.seek(0)  # 파일 포인터를 다시 처음으로
            next(reader)  # 헤더 건너뛰기

            print("\n데이터 가져오기 시작...")
            for row in tqdm(reader, total=total_rows - 1, desc="영화 데이터 처리 중"):
                try:
                    # 현재 처리 중인 영화 제목 출력
                    print(f"\n현재 처리 중: {row['title']}", end="\r")

                    movie, created = Movie.objects.update_or_create(
                        id=row["id"],
                        defaults={
                            "title": row["title"],
                            "revenue": row["revenue"],
                            "vote_average": row["vote_average"],
                            "imdb_id": row["imdb_id"],
                            "original_title": row["original_title"],
                            "overview": row["overview"],
                            "popularity": row["popularity"],
                            "genres": row["genres"],
                            "poster_path": row["poster_path"],
                            "keywords": row["keywords"],
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as e:
                    print(
                        f"\n오류 발생 - 영화 '{row.get('title', 'unknown')}' 처리 중: {str(e)}"
                    )
                    skipped_count += 1

            print("\n\n=== 가져오기 완료 ===")
            print(f"✅ 새로 생성된 영화: {created_count}")
            print(f"🔄 업데이트된 영화: {updated_count}")
            print(f"⚠️ 건너뛴 영화: {skipped_count}")
            print(f"📊 총 처리된 영화: {created_count + updated_count}")

    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {file_path}")
        print("Please make sure the CSV file exists in the dataset directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the CSV file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # 프로젝트 루트 디렉토리 기준으로 상대 경로 설정
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "./.."))
    csv_file_path = os.path.join(project_root, "dataset", "recent_movies.csv")

    print(f"Looking for CSV file at: {csv_file_path}")
    import_movies(csv_file_path)
