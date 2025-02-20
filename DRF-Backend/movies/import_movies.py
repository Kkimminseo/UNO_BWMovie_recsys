import os
import sys

# 프로젝트 루트를 sys.path에 추가하여 import 문제를 방지합니다.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Django 설정 모듈을 지정합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
import django

django.setup()

from movies.models import Genre

import csv
from datetime import datetime


def import_movies(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            Genre.objects.create(
                genre_name=row["genre"],
            )


if __name__ == "__main__":
    csv_file_path = "/Users/yongsu/UNO_BWMovie_recsys/dataset/genres.csv"
    import_movies(csv_file_path)
