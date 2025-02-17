from rest_framework import generics
from .serializers import UserSignUpSerializer, UserLogInSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
# 인증되지 않은 사용자도 접근 가능하게끔 해줌
from rest_framework import permissions
# status 문구 호출
from rest_framework import status
# refreshToken
from rest_framework_simplejwt.tokens import RefreshToken

# get_user_model() : Django에서 제공하는 함수
# AUTH_USER_MODEL로 커스텀 사용자 모델을 지정하면 get_user_model()은 그 커스텀 모델을 반환
User = get_user_model()

# 회원 가입 view
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [permissions.AllowAny]  # 모든 사용자가 접근 가능하도록 설정

# 로그인 view
class LogInView(generics.GenericAPIView):
    serializer_class = UserLogInSerializer
    # ⬇️ main/settings.py에 REST_FRAMEWORK 부문에 정의해둠
    permission_classes = [permissions.AllowAny] # AllowAny : 인증되지 않은 사용자도 접근 가능
    
    def post(self, request):
        # get_serializer : generics에 있어서 굳이 import 안 해도 사용 가능 
        seriarlizer = self.serializer_class(data=request.data) # serializer_class 직접 사용
        seriarlizer.is_valid(raise_exception=True) # raise_exception=True : 유효성 검사 실패 시, 예외 발생
        user = seriarlizer.validated_data['user']
        refresh = RefreshToken.for_user(user) # JWT 토큰 생성
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
            
# 로그아웃 view
class LogOutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated] # 로그인된 사람만 접근 가능
    
    def post(self, request):
        try:
            Refresh_token = request.data['refresh']
            token = RefreshToken(Refresh_token)
            token.blacklist() # 토큰을 블랙 리스트에 추가하여 해당 토큰이 더 이상 유효하지 않도록 함
            return Response({"message" : "로그아웃되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)