from django.db import models
from main.settings import AUTH_USER_MODEL  # AUTH USER MODEL 불러오기


# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # 채팅 참여자, 비회원 또한 채팅 참여 가능
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
