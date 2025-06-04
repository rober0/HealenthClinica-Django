from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Usuario
from .forms import RegistroForm, RegistroMedicoForm, LoginForm
from .decorators import user_redirect_handler

def register_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff or request.user.groups.filter(name='Administrador').exists():
            return redirect('dashboard:administrador')
        if request.user.groups.filter(name='Medico'.exists()):
            return redirect('dashboard:medicos')
        return redirect('dashboard:pacientes')

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            paciente_group = Group.objects.get(name='Paciente')
            user = Usuario.objects.create_user(username=username, email=email, password=password, grupo=paciente_group)
            user.groups.add(paciente_group)
            login(request, user)

            ''' if user.is_superuser or user.is_staff:
                administrador_group = Group.objects.get(name='Administrador')
                user.groups.add(administrador_group)
                user.grupo = administrador_group
                user.save()
                return redirect('dashboard:administrador') '''
            return redirect('dashboard:pacientes')
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {"form": form})

def login_view(request):

    error_message = None
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('dashboard:administrador')
        if request.user.groups.filter(name='Medico').exists():
            return redirect('dashboard:medicos')    
        return redirect('dashboard:pacientes')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser or user.is_staff:
                        return redirect('dashboard:administrador')
                    if request.user.groups.filter(name='Medico').exists():
                        return redirect('dashboard:medicos')    
                    return redirect('dashboard:pacientes')
                else:
                    error_message = "Senha inválida."
            except Usuario.DoesNotExist:
                error_message = "Email não encontrado."
    else:
        form = LoginForm()
            
    return render(request, 'users/login.html', {"form": form, "error": error_message})

def registermedicos_view(request):

    if request.method == "POST":
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Usuario.objects.create_user(username=username, email=email, password=password)
            login(request, user)

            paciente_group = Group.objects.get(name='Paciente')
            user.groups.add(paciente_group)

            if user.is_superuser or user.is_staff :
                administrador_group = Group.objects.get(name='Administrador')
                user.groups.add(administrador_group)
                return redirect('dashboard:administrador')
            return redirect('dashboard:pacientes')
    else:
        form = RegistroForm()
    return render(request, 'das/register.html', {"form": form}, {"all_medicos": all_medicos})
    
def registeradmin_view(request):

    if request.method == "POST":
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = Usuario.objects.create_user(username=username, email=email, password=password)
            login(request, user)

            paciente_group = Group.objects.get(name='Paciente')
            user.groups.add(paciente_group)

            if user.is_superuser or user.is_staff :
                administrador_group = Group.objects.get(name='Administrador')
                user.groups.add(administrador_group)
                return redirect('dashboard:administrador')
            return redirect('dashboard:pacientes')
    else:
        form = RegistroForm()
    return render(request, 'users/register.html', {"form": form}, {"all_admin": all_admin})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')
    else:
        return redirect('dashboard:pacientes')