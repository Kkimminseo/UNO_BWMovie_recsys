from rest_framework import generics
from .serializers import UserSignUpSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer