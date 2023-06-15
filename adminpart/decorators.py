from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    @wraps(view_func)
    @user_passes_test(lambda user: user.is_superuser)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return wrapper
