from django.shortcuts import redirect
from functools import wraps

def user_redirect_handler(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.is_staff:
            return redirect('dashboard:administrador')
        return function(request, *args, **kwargs)
    return wrap