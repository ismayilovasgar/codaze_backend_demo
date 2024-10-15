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
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("facebook/", FacebookLoginView.as_view(), name="facebook_login"),
    path("linkedin/", LinkedinLoginView.as_view(), name="linkedin_login"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    #
]
