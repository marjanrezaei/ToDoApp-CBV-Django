
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import TaskSerializer
from ...models import Task
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from .filters import TaskFilter

class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] 
    serializer_class = TaskSerializer 
    queryset = Task.objects.filter(completed=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']
    pagination_class = DefaultPagination 
    filterset_class = TaskFilter
    
   
   
    