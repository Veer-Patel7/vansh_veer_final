from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from hotels.models import Hotel, RoomType
from bookings.models import Booking
from reviews.models import Review
from django.db.models import Min, Max
from django.db import transaction
from django.core.mail import send_mail
from django.contrib import messages
from datetime import date
from decimal import Decimal
from django.conf import settings
from datetime import datetime


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, "customer/dashboard.html")

def customer_search(request):
    
    if request.user.is_authenticated and request.user.role in ["super_admin", "hotel_admin"]:
        return HttpResponse("Unauthorized")

    # ✅ CONTACT FORM
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            ['hotelpro1000@gmail.com'],
        )

    # ✅ SEARCH LOGIC
    location = request.GET.get("location")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")

    hotels = Hotel.objects.filter(status="LIVE").prefetch_related("rooms")

    if location:
        hotels = hotels.filter(city__icontains=location)

    hotels = hotels.annotate(
        min_price=Min("rooms__price_per_night"),
        max_price=Max("rooms__price_per_night")
    )

    if checkin and checkout:
        checkin = date.fromisoformat(checkin)
        checkout = date.fromisoformat(checkout)

        for hotel in hotels:
            total_available = 0
            for room in hotel.rooms.all():
                total_available += room.available_rooms(checkin, checkout)

            hotel.available_rooms = total_available
    else:
        for hotel in hotels:
            hotel.available_rooms = sum(
                room.total_rooms for room in hotel.rooms.all()
            )

    return render(request, "customer/search.html", {
        "hotels": hotels,
        "checkin": checkin,
        "checkout": checkout
    })

    # ✅ CONTACT FORM
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            ['hotelpro1000@gmail.com'],
        )

    # ✅ SEARCH LOGIC
    location = request.GET.get("location")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")

    hotels = Hotel.objects.all().filter(status="LIVE").prefetch_related("rooms")

    if location:
        hotels = hotels.filter(city__icontains=location)

    hotels = hotels.annotate(
        min_price=Min("rooms__price_per_night"),
        max_price=Max("rooms__price_per_night")
    )

    if checkin and checkout:
        checkin = date.fromisoformat(checkin)
        checkout = date.fromisoformat(checkout)

        for hotel in hotels:
            total_available = 0
            for room in hotel.rooms.all():
                total_available += room.available_rooms(checkin, checkout)

            hotel.available_rooms = total_available
    else:
        for hotel in hotels:
            hotel.available_rooms = sum(
                room.total_rooms for room in hotel.rooms.all()
            )

    return render(request, "customer/search.html", {
        "hotels": hotels,
        "checkin": checkin,
        "checkout": checkout
    })
        
@login_required
def profile_view(request):

    if not request.user.is_customer:
        return redirect("customer:home")   # or show permission page

    return render(request, "customer/profile.html")
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "customer/my_bookings.html", {"bookings": bookings})

def search_results(request):
    location = request.GET.get("location", "").strip()
    persons = request.GET.get("persons")

    rooms = RoomType.objects.select_related("hotel")

    if location:
        rooms = rooms.filter(hotel__address__icontains=location)

    if persons:
        rooms = rooms.filter(max_guest__gte=persons)

    return render(request, "customer/search_results.html", {"rooms": rooms})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    rooms = RoomType.objects.filter(hotel=hotel)

    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")

    if checkin and checkout:
        checkin = date.fromisoformat(checkin)
        checkout = date.fromisoformat(checkout)

        for room in hotel.rooms.all():
            room.available = room.available_rooms(checkin, checkout)

    return render(request, "customer/hotel_detail.html", {
        "hotel": hotel,
        "rooms": rooms
    })


def room_select(request, room_id):
    return render(request, "customer/room_select.html", {"room_id": room_id})


def booking_details(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(RoomType, id=room_id)

    if request.method == "POST":
        request.session["booking_data"] = {
            "hotel_id": hotel.id,
            "room_id": room.id,
            "checkin_date": request.POST.get("checkin_date"),
            "checkout_date": request.POST.get("checkout_date"),
            "total_guests": request.POST.get("total_guests"),
            "adults": request.POST.get("adults"),
            "children": request.POST.get("children"),
            "payment_method": request.POST.get("payment_method"),
        }
        return redirect("customer:confirm_booking")

    return render(request, "customer/booking_details.html", {
        "hotel": hotel,
        "room": room
    })


@login_required
def confirm_booking(request):

    data = request.session.get("booking_data")

    if not data:
        return redirect("customer:home")

    hotel = Hotel.objects.get(id=data["hotel_id"])
    room = RoomType.objects.get(id=data["room_id"])

    checkin = date.fromisoformat(data["checkin_date"])
    checkout = date.fromisoformat(data["checkout_date"])

    nights = (checkout - checkin).days
    total_price = nights * room.price_per_night

    if request.method == "POST":

        with transaction.atomic():

            room = RoomType.objects.select_for_update().get(id=data["room_id"])

            # Count existing bookings
            booked_rooms = Booking.objects.filter(
                room=room,
                checkin_date__lt=checkout,
                checkout_date__gt=checkin
            ).count()

            # Calculate available rooms
            available = room.total_rooms - booked_rooms

            if available <= 0:
                messages.error(request, "No rooms available for selected dates")
                return redirect("customer:hotel_detail", id=room.hotel.id)

            # Create booking
            Booking.objects.create(
                user=request.user,
                hotel_id=data["hotel_id"],
                room_id=data["room_id"],
                checkin_date=checkin,
                checkout_date=checkout,
                total_guests=data["total_guests"],
                adults=data["adults"],
                children=data["children"],
                payment_method=data["payment_method"],
                total_price=total_price
            )

        del request.session["booking_data"]

        return redirect("customer:booking_success")

    return render(request, "customer/confirm_booking.html", {
        "data": data,
        "room": room,
        "hotel": hotel,
        "nights": nights,
        "total_price": total_price
    })    

@login_required
def booking_success(request):
    if request.method == "POST":
        return redirect("customer:home")
    return render(request, "customer/success.html")


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

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        send_mail(
            subject,
            full_message,
            email,
            ['hotelpro1000@gmail.com'],
        )

    return render(request, "contact.html")