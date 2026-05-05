from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    POST /api/register/
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Получение JWT токена.
    POST /api/token/
    """
    serializer_class = CustomTokenObtainPairSerializer