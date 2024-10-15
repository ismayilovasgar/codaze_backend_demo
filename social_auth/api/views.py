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


# -------------------------------------------------------------------------------------------------------
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user_info = self.validate_google_token(token)

        if not user_info:
            return Response(
                {"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})

    def validate_google_token(self, token):
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None


class FacebookLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user_info = self.validate_facebook_token(token)

        if not user_info:
            return Response(
                {"error": "Invalid Facebook token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "first_name": user_info.get("first_name", ""),
                "last_name": user_info.get("last_name", ""),
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})

    def validate_facebook_token(self, token):
        url = f"https://graph.facebook.com/me?fields=id,email,first_name,last_name&access_token={token}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None


class LinkedInLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        user_info = self.validate_linkedin_token(token)

        if not user_info:
            return Response(
                {"error": "Invalid LinkedIn token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(
            email=user_info["emailAddress"],
            defaults={
                "first_name": user_info.get("localizedFirstName", ""),
                "last_name": user_info.get("localizedLastName", ""),
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})

    def validate_linkedin_token(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        url = "https://api.linkedin.com/v2/me"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            email_response = requests.get(
                "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
                headers=headers,
            )
            if email_response.status_code == 200:
                profile = response.json()
                email = email_response.json()["elements"][0]["handle~"]["emailAddress"]
                profile["emailAddress"] = email
                return profile

        return None
