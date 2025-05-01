from django.urls import path
from . import views

app_name = "accounting"

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
     path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

]