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
   - 'dataset' 폴더에 'revised_df.csv' 파일 위치

4. 스크립트 실행:
   python -m movies.import_movies
"""

import os
import sys

# 프로젝트 루트를 sys.path에 추가하여 import 문제를 방지합니다.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

// ... existing code ...

import os
import sys

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
            count = 0
            for row in reader:
                try:
                    Movie.objects.create(
                        id=row["id"],
                        title=row["title"],
                        revenue=row["revenue"],
                        vote_average=row["vote_average"],
                        imdb_id=row["imdb_id"],
                        original_title=row["original_title"],
                        overview=row["overview"],
                        popularity=row["popularity"],
                        genres=row["genres"],
                        poster_path=row["poster_path"],
                        keywords=row["keywords"],
                    )
                    count += 1
                except Exception as e:
                    print(
                        f"Error importing movie {row.get('title', 'unknown')}: {str(e)}"
                    )
            print(f"Successfully imported {count} movies")
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {file_path}")
        print("Please make sure the CSV file exists in the dataset directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the CSV file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    # 프로젝트 루트 디렉토리 기준으로 상대 경로 설정
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    csv_file_path = os.path.join(project_root, "dataset", "revised_df.csv")

    print(f"Looking for CSV file at: {csv_file_path}")
    import_movies(csv_file_path)
