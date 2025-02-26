from django.db import models
from django.contrib.auth.models import AbstractUser

# 기본 user 모델
class User(AbstractUser):
    # 원하는 필드 추가하기
    nickname = models.CharField(max_length=30, blank=True)
    
    # 객체의 문자열 표현 정리 : User를 view에서 쓸 때 username이 return 됨, username말고 다른 거 해도 됨
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "사용자" # 관리자 페이지에서 보여지는 단수 이름
        verbose_name_plural = "사용자 목록" # 관리자 페이지에서 보여지는 복수 이름