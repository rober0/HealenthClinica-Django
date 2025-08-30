from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, "administrador"):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


def medico_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, "medico"):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


def paciente_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, "paciente"):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap
