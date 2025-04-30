from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.BaseView.as_view(), name='base-view'),
    
]
