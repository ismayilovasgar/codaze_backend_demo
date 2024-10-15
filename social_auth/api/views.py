#
## <== Social Login - Google,Facebook,LinkedIn ==>
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.linkedin import LinkedinOAuth2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        strategy = load_strategy(request)
        backend = GoogleOAuth2(strategy=strategy)
        try:
            user = backend.do_auth(token)
            if user and user.is_active:
                # Kullanıcıyı doğrula ve JWT üret
                return Response({"message": "Google login successful"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FacebookLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        strategy = load_strategy(request)
        backend = FacebookOAuth2(strategy=strategy)
        try:
            user = backend.do_auth(token)
            if user and user.is_active:
                return Response({"message": "Facebook login successful"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LinkedinLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        strategy = load_strategy(request)
        backend = LinkedinOAuth2(strategy=strategy)
        try:
            user = backend.do_auth(token)
            if user and user.is_active:
                return Response({"message": "LinkedIn login successful"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            # Şifre sıfırlama bağlantısını veya kodunu e-posta ile gönderin
            return Response({"message": "Password reset email sent"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
