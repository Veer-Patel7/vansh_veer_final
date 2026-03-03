from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hotels.models import Hotel
from reviews.models import Review
from django.db.models import Min, Max
@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "customer/dashboard.html")

def customer_search(request):
    hotels = Hotel.objects.all()

    location = request.POST.get("location")

    if location:
        hotels = hotels.filter(city__icontains=location)

    # Add min and max price from related rooms
    # hotels = hotels.annotate(
    #     min_price=Min("rooms__category__price_per_night"),
    #     max_price=Max("rooms__category__price_per_night")
    # )
        
    return render(request, "customer/search.html", {
        "hotels": hotels
    })

def search_results(request):
    if request.method == "POST":
        city = request.POST.get("city")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        # For simplicity, we are not filtering based on availability in this example
        hotels = Hotel.objects.filter(city__icontains=city)

        return render(request, "customer/search_results.html", {"hotels": hotels})

    return redirect("hotel_detail")

def hotel_detail(request, hotel_id):
    return render(request, "customer/hotel_detail.html", {"hotel_id": hotel_id})

def room_select(request, room_id):
    return render(request, "customer/room_select.html", {"room_id": room_id})

@login_required(login_url="/login/")
def booking_details(request):
    return render(request, "customer/booking_details.html")

@login_required(login_url="/login/")
def add_review(request, hotel_id):

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        recommend = request.POST.get("recommend")

        Review.objects.create(
            hotel_id=hotel_id,
            user=request.user,
            rating=rating,
            comment=comment,
            recommend=True if recommend == "yes" else False
        )

        return redirect("/")

    return render(request, "customer/add_review.html")