import re
from rest_framework import generics
from .serializers import UserSignUpSerializer, UserLogInSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware.csrf import get_token
# 인증되지 않은 사용자도 접근 가능하게끔 해줌
from rest_framework import permissions

# status 문구 호출
from rest_framework import status

# refreshToken
from rest_framework_simplejwt.tokens import RefreshToken

# get_user_model() : Django에서 제공하는 함수
# AUTH_USER_MODEL로 커스텀 사용자 모델을 지정하면 get_user_model()은 그 커스텀 모델을 반환
User = get_user_model()

def get_csrf_token(request):
    csrf_token = get_token(request)
    response = JsonResponse({"csrfToken": csrf_token})
    response.set_cookie(
        key="csrftoken",
        value=csrf_token,
        httponly=False,  # ✅ React에서 쿠키를 읽을 수 있도록 수정
        secure=False,    
        samesite="Lax"
    )
    return response


# 회원 가입 view
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]  # 모든 사용자가 접근 가능하도록 설정

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # 새로운 사용자 저장
            return Response({"message": "회원가입 성공!", "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 view
class LogInView(generics.GenericAPIView):
    serializer_class = UserLogInSerializer
    permission_classes = [permissions.AllowAny]  # 인증되지 않은 사용자도 접근 가능

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)  # JWT 토큰 생성
            return Response(
                {
                    "message": "로그인 성공!",
                    "status": "ok",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "username": user.username,
                        "nickname": user.nickname,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 로그아웃 view
class LogOutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # 로그인된 사용자만 접근 가능

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  # refresh 토큰 가져오기
            if not refresh_token:
                return Response({"error": "토큰이 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰을 블랙리스트에 추가하여 무효화
            return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
