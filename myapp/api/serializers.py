from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers  # Import the serializer class
from ..models import Note  # Import the Note model
from ..models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# Create a serializer class
# This class will convert the Note model into JSON
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # username = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password2", "bio", "cover_photo")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            bio=validated_data["bio"],
            cover_photo=validated_data["cover_photo"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
