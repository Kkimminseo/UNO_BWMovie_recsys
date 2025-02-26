from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True)  # 메시지 필수 입력

    class Meta:  # 모델 설정
        model = Chat
        fields = ["message"]
