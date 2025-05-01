from django.views.generic.edit import FormView
from accounts.forms import CustomUserCreationForm

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/task/' # Redirect to login after successful signup

    def form_valid(self, form):
        form.save()  # Save the user to the database
        return super().form_valid(form)