from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)        
    return wrapper_func

def is_BUH_SALES_INCHARGE(view_func):
    pass