from django.urls import reverse
from django.shortcuts import redirect

def login_required_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))  # Redirect to the login page
        return view_func(request, *args, **kwargs)
    return wrapper