from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='users:login')
def pacientes(request):
    return render(request, 'dashboard/dashboardpac.html')

@login_required(login_url='users:login')
def medicos(request):
    return render(request, 'dashboard/dashboardmed.html')