from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Contact
from .serializers import ContactSerializer

@api_view(['POST'])
def create_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reset_contact_form(request):
    empty_form = {
        "name": "",
        "surname": "",
        "email": "",
        "title": "",
        "content": ""
    }
    return Response(empty_form, status=status.HTTP_200_OK)