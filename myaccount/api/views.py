from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from ..models import CustomUser
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's refresh token from the request
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)

            # Blacklist the token
            token.blacklist()

            return Response({"detail": "Logout successful."}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# class RegisterView(APIView):
#     User = get_user_model()
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         email = request.data.get("email")

#         # Kullanıcı oluştur
#         if User.objects.filter(username=username).exists():
#             return Response({"detail": "Bu kullanıcı adı zaten alınmış."}, status=400)

#         user = User.objects.create_user(
#             username=username, password=password, email=email
#         )

#         # JWT Token oluştur
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         # Token'ları veritabanına kaydet
#         Token.objects.create(
#             user=user, access_token=access_token, refresh_token=refresh_token
#         )

#         return Response(
#             {
#                 "username": user.username,
#                 "email": user.email,
#                 "access": access_token,
#                 "refresh": refresh_token,
#             },
#             status=status.HTTP_201_CREATED,
#         )
