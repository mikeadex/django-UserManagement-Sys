from django.http import HttpResponseForbidden
from functools import wraps


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not allowed to access this page")
        return _wrapped_view
    return decorator
