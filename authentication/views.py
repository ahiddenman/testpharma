from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})

class LoginView(auth_views.LoginView):
    template_name = "authentication/login.html"
    form_class = AuthenticationForm

class LogoutView(auth_views.LogoutView):
    template_name = "authentication/logout.html"
