from django.shortcuts import redirect
from functools import wraps
from django.core.exceptions import PermissionDenied
from users.models import Administrador, Medico, Paciente

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or isinstance(request.user, Administrador):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def medico_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            medico = Medico.objects.get(email=request.user.email)
            return function(request, *args, **kwargs)
        except Medico.DoesNotExist:
            raise PermissionDenied
    return wrap

def paciente_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            paciente = Paciente.objects.get(email=request.user.email)
            return function(request, *args, **kwargs)
        except Paciente.DoesNotExist:
            raise PermissionDenied
    return wrap