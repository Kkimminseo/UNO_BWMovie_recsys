from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.conf import settings
from .serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated
import openai


class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_message = serializer.validated_data.get("message")

        try:
            # 채팅 메시지 저장
            chat = serializer.save(user=request.user)

            openai.api_key = settings.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Answer in Korean.",
                    },
                    {"role": "user", "content": user_message},
                ],
            )
            chat_response = response.choices[0].message["content"]
            return Response({"message": chat_response}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"요청 처리 중 오류가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
