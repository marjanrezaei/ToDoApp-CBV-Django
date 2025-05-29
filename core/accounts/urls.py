from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('', include('django.contrib.auth.urls')),
    path("api/v1/", include("accounts.api.v1.urls")),
    path("send-email/", views.send_email, name="send_email"),


]