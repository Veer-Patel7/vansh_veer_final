from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from django.core.mail import send_mail
from django.conf import settings

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


@login_required
def add_review(request, hotel_id):

    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        recommend = request.POST.get("recommend")

        # convert recommend string to boolean
        recommend_value = True if recommend == "True" else False

        Review.objects.create(
            hotel=hotel,
            user=request.user,
            rating=rating,
            comment=comment,
            recommend=recommend_value
        )

        # Send email to admin
        subject = "New Hotel Review Submitted"

        message = f"""
        Hotel Name : {hotel.hotel_name}
        Customer : {request.user.email}
        Rating : {rating}
        Recommend : {recommend_value}

        Comment :
        {comment}
        """

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            ["admin@gmail.com"],   # admin email
            fail_silently=False,
        )

        messages.success(request, "Review submitted successfully")
        return redirect("hotel_detail", hotel_id=hotel.id)
