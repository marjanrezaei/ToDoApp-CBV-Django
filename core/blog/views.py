from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm

# Create your views here.
class BaseView(TemplateView):
    template_name = 'base.html'
    
    def get_context_data(self, **kwargs):
        """
        a class based view to show base page.
        """
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context
    

class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 2  
    ordering = '-id'
    

class TaskDetailView(DetailView):
    model = Task
    
    
class TaskCreateView(CreateView):
    model = Task
    # fields = ['author', 'title', 'description', 'completed']
    form_class = TaskForm
    success_url = '/blog/task/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    
class TaskEditView(UpdateView):
    model = Task
    form_class = TaskForm
    success_url = '/blog/task/'
    
    
class TaskDeleteView(DeleteView):
    model = Task
    success_url = '/blog/task/'
    