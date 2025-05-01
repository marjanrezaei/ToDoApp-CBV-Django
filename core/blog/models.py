from django.db import models
# from accounts.models import Profile

# User = get_user_model()

# Create your models here.
class Task(models.Model):
    '''
    this is a class to define tasks for todo app
    '''
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title