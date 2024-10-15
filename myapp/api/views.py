from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        # Kullanıcıyı kaydet
        user = serializer.save()

        # Auth Token oluştur ve kaydet
        token, created = Token.objects.get_or_create(user=user)

        # Token'ı yanıt olarak döndürebiliriz
        self.token = token.key

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["token"] = self.token  # Token'ı yanıt verisine ekle
        return response
