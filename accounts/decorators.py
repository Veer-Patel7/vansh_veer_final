from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def customer_required(view_func):
    """
    Decorator for views that checks that the logged in user is a customer.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer,
        login_url='account:login'
    )
    return actual_decorator(view_func)

def hotel_admin_required(view_func):
    """
    Decorator for views that checks that the logged in user is a hotel admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_hotel_admin,
        login_url='account:login'
    )
    return actual_decorator(view_func)

def super_admin_required(view_func):
    """
    Decorator for views that checks that the logged in user is a super admin.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_super_admin,
        login_url='account:login'
    )
    return actual_decorator(view_func)
