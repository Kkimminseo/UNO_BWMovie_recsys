from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import ChatSerializer
from rest_framework.permissions import AllowAny
import openai


# Create your views here.
class ChatAPIView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):  # 채팅 생성
        serializer = self.get_serializer(
            data=request.data
        )  # 유저입력한 데이터를 시리얼라이저에 저장
        serializer.is_valid(raise_exception=True)  # 유효성 검사
        user_message = serializer.validated_data.get("message")  # 유저가 입력한 메시지

        try:  # GPT-3.5 turbo 모델을 사용하여 채팅 생성
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
            return Response(
                {"message": chat_response}, status=status.HTTP_200_OK
            )  # 채팅 응답 반환
        except Exception:
            return Response(
                {"message": "An error occurred while processing your request."},
                status=status.HTTP_400_BAD_REQUEST,
            )  # 에러 발생시 반환
