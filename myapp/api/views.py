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


# Create your views here.
# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# api/profile  and api/profile/update
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# api/notes
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNotes(request):
    public_notes = Note.objects.filter(is_public=True).order_by("-updated")[:10]
    user_notes = request.user.notes.all().order_by("-updated")[:10]
    notes = public_notes | user_notes
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)
