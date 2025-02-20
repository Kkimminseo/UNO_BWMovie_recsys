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
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
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


if __name__ == "__main__":
    csv_file_path = "/Users/yongsu/UNO_BWMovie_recsys/dataset/revised_df.csv"
    import_movies(csv_file_path)
