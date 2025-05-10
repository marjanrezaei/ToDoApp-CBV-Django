from rest_framework import generics
from django_filters import rest_framework as filters
from ...models import Task

class TaskFilter(filters.FilterSet):
    """Filter for Task model"""
    class Meta:
        model = Task
        fields = {
            'title': ['exact', 'in'],
            'author': ['exact'],
        }
        
        