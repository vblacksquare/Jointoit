
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        max_length=settings.MAX_PASSWORD_LENGTH,
        style={'input_type': 'password'}
    )
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def create(self, validated_data):
        email = validated_data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            return user

        return User.objects.create_user(
            is_active=False,
            **validated_data
        )

    def validate_name(self, value):
        has_not_letter = any(char not in settings.ALLOWED_USERNAME_CHARS for char in value)

        if has_not_letter:
            raise serializers.ValidationError("Name has to contain only latin characters, digits and '-', '_'")

        if len(value) > settings.MAX_USERNAME_LENGTH:
            raise serializers.ValidationError(f"Name is longer than {settings.MAX_USERNAME_LENGTH} chars")

        return value

    def validate_email(self, value):
        value = value.lower()

        validate_email(value)

        user = User.objects.filter(email=value.lower()).first()
        if user:
            raise serializers.ValidationError("Email already exists")

        return value

    def validate_password(self, value):
        validate_password(value, user=self.instance)
        return value


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        if not user.is_active:
            raise AuthenticationFailed("Email not verified")

        return data


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        max_length=settings.MAX_PASSWORD_LENGTH,
        style={'input_type': 'password'}
    )

    def validate_password(self, value):
        validate_password(value)
        return value
