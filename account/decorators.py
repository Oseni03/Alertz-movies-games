from django.http import HttpResponse 
from django.shortcuts import redirect 


def subscription_required(view_func):
    
    def wrapper_func(request, *args, **kwargs):
        if not request.user.subscription:
            return redirect("alert:checkout")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper


def anonymous_required(view_func):
    
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("account:dashboard")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
