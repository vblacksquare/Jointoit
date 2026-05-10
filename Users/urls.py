
from django.urls import path
from .views import (
    LoginView, RegisterView,
    VerifyEmailView, TokenRefreshView,
    ForgotPasswordView, ResetPasswordView,
    LogoutView
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("verify/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name='login'),
    path("refresh/", TokenRefreshView.as_view(), name='refresh-login'),
    path("forgot/", ForgotPasswordView.as_view(), name='forgot'),
    path("reset/", ResetPasswordView.as_view(), name='reset'),
    path("logout/", LogoutView.as_view(), name='logout'),
]
