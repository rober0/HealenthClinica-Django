from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paciente, Medico, Administrador
from .forms import RegistroForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        if isinstance(request.user, Administrador):
            return redirect('dashboard:administrador')
        elif isinstance(request.user, Medico):
            return redirect('dashboard:medicos')
        elif isinstance(request.user, Paciente):
            return redirect('dashboard:pacientes')
    
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard:pacientes')
                else:
                    messages.error(request, "Erro ao fazer login automático.")
            except Exception as e:
                messages.error(request, f"Erro ao criar conta: {str(e)}")
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.user.is_authenticated:
        if isinstance(request.user, Administrador):
            return redirect('dashboard:administrador')
        elif isinstance(request.user, Medico):
            return redirect('dashboard:medicos')
        elif isinstance(request.user, Paciente):
            return redirect('dashboard:pacientes')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if isinstance(user, Administrador):
                    return redirect('dashboard:administrador')
                elif isinstance(user, Medico):
                    return redirect('dashboard:medicos')
                else:
                    return redirect('dashboard:pacientes')
            else:
                messages.error(request, 'Email ou senha inválidos.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'error_message': error_message})

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')