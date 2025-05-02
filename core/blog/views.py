from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Profile


class BaseView(TemplateView):
    template_name = 'base.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.session['user_id'] = request.user.id
            try:
                profile = Profile.objects.get(user=request.user)
                request.session['first_name'] = profile.first_name
            except Profile.DoesNotExist:
                request.session['first_name'] = ''  # Handle missing profile gracefully
        
        return super().dispatch(request, *args, **kwargs)
    

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 2

    def get_queryset(self):
        # Filter queryset to show only tasks for the logged-in user
        return Task.objects.filter(author__user__email=self.request.user).order_by('-id')

        
    


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    # fields = ['author', 'title', 'description', 'completed']
    form_class = TaskForm
    success_url = '/task/'
    
    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile 
        return super().form_valid(form)
        
    
class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/task/'
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/task/'
    
    
    
