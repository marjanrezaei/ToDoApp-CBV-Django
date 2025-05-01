from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseView(TemplateView):
    template_name = 'base.html'
    
    def get_context_data(self, **kwargs):
        """
        A class-based view to show the base page.
        """
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.filter(author__user__email=self.request.user)  # Corrected filter
        if tasks.exists():  # Prevent errors if queryset is empty
            context['names'] = tasks.first().author
        else:
            context['names'] = None  # Handle case when no tasks exist
        return context
    

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        # Filter queryset to show only tasks for the logged-in user
        return Task.objects.filter(author__user__email=self.request.user)

        
    


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    # fields = ['author', 'title', 'description', 'completed']
    form_class = TaskForm
    success_url = '/task/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    
class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/task/'
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/task/'
    
    
    
