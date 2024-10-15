from django.contrib import admin
from django.urls import path, include
from . import views

# from .. import views as note_views

from .views import (
    GoogleLoginView,
    FacebookLoginView,
    LinkedinLoginView,
    ResetPasswordView,
)


urlpatterns = [
    # Social Login Account / Foreget Password
    path("auth/google/", GoogleLoginView.as_view(), name="google_login"),
    path("auth/facebook/", FacebookLoginView.as_view(), name="facebook_login"),
    path("auth/linkedin/", LinkedinLoginView.as_view(), name="linkedin_login"),
    path("auth/reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    #
]
