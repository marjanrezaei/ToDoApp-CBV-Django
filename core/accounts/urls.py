from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('', include('django.contrib.auth.urls')),

]