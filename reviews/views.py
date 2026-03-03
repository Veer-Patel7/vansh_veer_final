from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Review

# HOTEL ADMIN → request delete
@login_required(login_url="/hotel/login/")
def request_delete(request, id):
    r = Review.objects.get(id=id)
    r.status = "delete_request"
    r.save()
    return redirect("/hotel/dashboard/")


# SUPER ADMIN → approve delete
@login_required(login_url="/super/")
def approve_delete(request, id):
    r = Review.objects.get(id=id)
    r.status = "deleted"
    r.save()
    return redirect("/super/reviews/")


# SUPER ADMIN → reject delete
@login_required(login_url="/super/")
def reject_delete(request, id):
    r = Review.objects.get(id=id)
    r.status = "active"
    r.save()
    return redirect("/super/reviews/")