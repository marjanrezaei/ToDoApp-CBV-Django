from django.views.generic.edit import FormView
from accounts.forms import CustomUserCreationForm
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm 


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/accounts/login/' # Redirect to login after successful signup

    def form_valid(self, form):
        form.save()  # Save the user to the database
        return super().form_valid(form)
       

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    form_class = ProfileForm
    success_url = "/"  # Redirect after successful update

    def get_object(self):
        return Profile.objects.get(user=self.request.user)  # Get the logged-in user's profile
