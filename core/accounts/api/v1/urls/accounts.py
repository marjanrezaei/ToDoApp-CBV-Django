from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # registration
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    path("test-email", views.TestEmailSend.as_view(), name="test-email"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend",
        views.ResendActivationApiView.as_view(),
        name="resend-activation",
    ),
    # change password
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # reset password
    path(
        "reset-password/",
        views.ResetPasswordApiView.as_view(),
        name="reset-password",
    ),
    path(
        "reset-password/confirm/<str:token>",
        views.ResetPasswordConfirmApiView.as_view(),
        name="reset-password-confirm",
    ),

    # login jwt
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
