
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    RegisterSerializer, TokenSerializer,
    ForgotPasswordSerializer, VerifyEmailSerializer,
    ResetPasswordSerializer
)
from .services import EmailService

import logging


logger = logging.getLogger(__name__)

User = get_user_model()


def logout(user):
    tokens = OutstandingToken.objects.filter(user=user)
    for token in tokens:
        BlacklistedToken.objects.get_or_create(token=token)


class RegisterView(APIView):

    @extend_schema(
        summary="Register a new user",
        request=RegisterSerializer,
        responses={
            200: OpenApiResponse(description="Email sent successfully")
        },
        tags=["Users"]
    )
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            if user.is_active:
                logger.info(f"Register attemp: user already exists -> {user}")

                return Response({
                    "error": "User with this email or username already exists"
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                logger.info(f"Register attemp: resend verification -> {user}")

                EmailService.verify_email(user)

                return Response({
                    "message": "Check your email to verify account"
                })

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        try:
            EmailService.verify_email(user)

        except Exception as err:
            user.delete()

            logger.error(f"Register attemp: email service down -> {user}")
            logger.exception(err)

            return Response({
                "error": "Users service is down now. Please try again later"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Register attemp: send verification -> {user}")

        return Response({
            "message": "Check your email to verify account"
        })


class VerifyEmailView(APIView):

    @extend_schema(
        summary="Verify a new user",
        request=VerifyEmailSerializer,
        responses={
            200: OpenApiResponse(description="Email confirmed")
        },
        tags=["Users"]
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({
                "error": "Invalid code"
            }, status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get(f"verify:{user.id}")
        if not cached_code or cached_code != code:
            return Response({
                "error": "Invalid code"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        cache.delete(f"verify:{user.id}")

        return Response({"message": "verified"})


class ForgotPasswordView(APIView):

    @extend_schema(
        summary="Forgot password",
        request=ForgotPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Reset password email sent")
        },
        tags=["Users"]
    )
    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if user:
            try:
                EmailService.reset_password(user=user)

                logger.info(f"Password reset email sent -> {user}")

            except Exception as err:
                logger.error(f"Password reset failed -> {user}")
                logger.exception(err)

        return Response({
            "message": "If account exists, reset email was sent"
        })


class ResetPasswordView(APIView):

    @extend_schema(
        summary="Reset password",
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password changed")
        },
        tags=["Users"]
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get("email")
        code = serializer.validated_data['code']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({
                "error": "Invalid code"
            }, status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get(f"reset:{user.id}")
        if not cached_code or cached_code != code:
            return Response({
                "error": "Invalid code"
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        cache.delete(f"reset:{user.id}")
        logout(user)

        return Response({"message": "Changed password"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout",
        responses={
            200: OpenApiResponse(description="Logged out")
        },
        tags=["Users"]
    )
    def get(self, request):
        logout(request.user)

        return Response({"message": "Logged out"})


@extend_schema(
    summary="Login",
    tags=["Users"],
)
class LoginView(TokenObtainPairView):
    serializer_class = TokenSerializer


@extend_schema(
    summary="Refresh login",
    tags=["Users"],
)
class TokenRefreshView(TokenRefreshView):
    pass
