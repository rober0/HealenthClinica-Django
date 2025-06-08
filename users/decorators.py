from django.shortcuts import redirect
from functools import wraps
from django.core.exceptions import PermissionDenied
from users.models import Administrador, Medico, Paciente

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if isinstance(request.user, Administrador):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def medico_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if isinstance(request.user, Medico):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap

def paciente_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if isinstance(request.user, Paciente):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap