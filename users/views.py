from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paciente, Medico, Administrador, Contato
from .forms import RegistroForm, LoginForm, ContatoForm


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or isinstance(request.user, Administrador):
            return redirect("dashboard:administrador")
        elif isinstance(request.user, Medico):
            return redirect("dashboard:medicos")
        elif isinstance(request.user, Paciente):
            return redirect("dashboard:pacientes")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect("dashboard:pacientes")

            except Exception as e:
                messages.error(request, f"Erro ao criar conta: {str(e)}")
    else:
        form = RegistroForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or isinstance(request.user, Administrador):
            return redirect("dashboard:administrador")
        elif isinstance(request.user, Medico):
            return redirect("dashboard:medicos")
        elif isinstance(request.user, Paciente):
            return redirect("dashboard:pacientes")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                if user.is_superuser:
                    return redirect("dashboard:administrador")

                try:
                    admin = Administrador.objects.get(email=email)
                    return redirect("dashboard:administrador")
                except Administrador.DoesNotExist:
                    try:
                        medico = Medico.objects.get(email=email)
                        return redirect("dashboard:medicos")
                    except Medico.DoesNotExist:
                        try:
                            paciente = Paciente.objects.get(email=email)
                            return redirect("dashboard:pacientes")
                        except Paciente.DoesNotExist:
                            messages.error(request, "Tipo de usuário não identificado.")
            else:
                messages.error(request, "Email ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("users:login")



def contato_view(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("templates:contact-us")
    else:
        form = ContatoForm()

    return render(request, "templates/faleconosco.html", {"form": form})