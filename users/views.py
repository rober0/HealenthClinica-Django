from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import RegistroForm, LoginForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard:pacientes')
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {"form": form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard:pacientes')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {"form": form})

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('/')

