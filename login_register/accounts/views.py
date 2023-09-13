from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


class Home(TemplateView):
    template_name = "home.html"

def index(request):
    return render(request,'index.html')
class SignUpView(CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

def user_login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the dashboard page upon successful login
        else:
            # Handle login failure
            pass
    return render(request, 'registration/login.html')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to the dashboard page upon successful registration and login
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
