from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('base', views.BaseView.as_view(), name='base-view'),
    path('task/', views.TaskListView.as_view(), name="task-list"),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('task/create/', views.TaskCreateView.as_view(), name="task-create"),
    path('task/<int:pk>/edit/', views.TaskEditView.as_view(), name="task-edit"),
    
]
