from django.db import models
from django.contrib.auth.models import AbstractUser

# 관심사 선택하는 모델
class Interest(models.Model):
    # name : 관심사 이름을 저장하는 필드
    # unique=True 옵션을 사용하여 중복된 관심사가 저장되지 않도록 함
    name = models.CharField(max_length=50, unique=True)
    
    # 객체를 문자열로 표현할 때 관심사 이름을 반환하도록 함
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "관심사" # 관리자 페이지에서 보여지는 단수 이름
        verbose_name_plural = "관심사 목록" # 관리자 페이지에서 보여지는 복수 이름

# 기본 user 모델
class User(AbstractUser):
    # 원하는 필드 추가하기
    nickname = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True, verbose_name="관심사")
    
    # 객체의 문자열 표현 정리 : User를 view에서 쓸 때 username이 return 됨, username말고 다른 거 해도 됨
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "사용자" # 관리자 페이지에서 보여지는 단수 이름
        verbose_name_plural = "사용자 목록" # 관리자 페이지에서 보여지는 복수 이름