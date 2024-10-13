from django.contrib import admin
from django.urls import path, include
from . import views
from .. import views as note_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Authentication
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),

    # Profile
    path("profile/", note_views.getProfile, name="profile"),
    path("profile/update/", note_views.updateProfile, name="update-profile"),
    
    # Notes
    path("notes/", note_views.getNotes, name="notes"),
    path("notes/<int:pk>/", note_views.getNote, name="note"),
    path("notes/<int:pk>/update/", note_views.updateNote, name="update-note"),
    path("notes/<int:pk>/delete/", note_views.deleteNote, name="delete-note"),
    path("users/<int:pk>/notes", note_views.getUserNotes, name="my-notes"),
    path("notes/create/", note_views.createNote, name="create-note"),
]
