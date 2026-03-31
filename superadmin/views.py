from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from hotels.models import ChangeRequest, Hotel, RoomType, HotelImage
from accounts.models import User
from bookings.models import Booking
from payments.models import HotelCommission
from datetime import date, timedelta
from django.conf import settings
from reviews.models import Review
from datetime import date, timedelta, datetime
from django.db.models import Sum, Q, F, ExpressionWrapper, DecimalField
from decimal import Decimal
from django.contrib import messages


User = get_user_model()

# ================= Dashboard =================  
@login_required(login_url="/super/")
def dashboard(request):
    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")
        
    # Hotel Stats
    hotels = Hotel.objects.all()
    hotel_stats = {
        'total': hotels.count(),
        'pending': hotels.filter(status="PENDING").count(),
        'live': hotels.filter(status="LIVE").count(),
    }
    
    # User Stats
    total_owners = User.objects.filter(role="hotel_admin").count()
    total_customers = User.objects.filter(role="customer").count()
    
    # Financial Stats
    commissions = HotelCommission.objects.all()
    total_revenue = sum([c.commission_amount for c in commissions if c.status == 'paid'])
    pending_revenue = sum([c.commission_amount for c in commissions if c.status == 'pending'])
    
    # Booking Stats
    total_bookings = Booking.objects.count()

    # Update Requests
    pending_updates = ChangeRequest.objects.filter(status="PENDING").count()
    
    # Recent Activities
    recent_hotels = Hotel.objects.all().order_by('created_at')[:5]
    
    context = {
        'hotel_stats': hotel_stats,
        'total_owners': total_owners,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'total_bookings': total_bookings,
        'pending_updates': pending_updates,
        'recent_hotels': recent_hotels,
    }
    
    return render(request, "superadmin/dashboard.html", context)

# ================= profile =================
@login_required
def profile(request):

    if request.method == "POST":

        # PROFILE UPDATE
        if "username" in request.POST:

            request.user.username = request.POST.get("username")
            request.user.email = request.POST.get("email")

            if request.FILES.get("profile_photo"):
                request.user.profile_photo = request.FILES.get("profile_photo")

            request.user.save()

            messages.success(request, "Profile updated successfully")
            return redirect("/super/profile/")


        # PASSWORD CHANGE
        if "old_password" in request.POST:

            old = request.POST.get("old_password")
            new = request.POST.get("new_password")
            confirm = request.POST.get("confirm_password")

            user = request.user

            if not user.check_password(old):
                messages.error(request, "Old password incorrect")
                return redirect("/super/profile/")

            if new != confirm:
                messages.error(request, "Passwords do not match")
                return redirect("/super/profile/")

            user.set_password(new)
            user.save()

            messages.success(request, "Password updated successfully")
            return redirect("/super/")


    context = {
        "hotels_count": Hotel.objects.count(),
        "bookings_count": Booking.objects.count(),
        "customers_count": User.objects.filter(role="customer").count()
    }

    return render(request, "superadmin/profile.html", context)

# ================= hotel-owner manage =================
@login_required(login_url="/super/")
def owners(request):
    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    search = request.GET.get("search")
    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")

    owners = User.objects.filter(role="hotel_admin")

    if search:
        if search.isdigit():
            owners = owners.filter(id=int(search))
        else:
            owners = owners.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Status search
        if search.lower() == "active":
            owners = User.objects.filter(role="hotel_admin", is_active=True)

        if search.lower() == "pending":
            owners = User.objects.filter(role="hotel_admin", is_active=False)

        # Action search
        if search.lower() == "approve":
            owners = User.objects.filter(role="hotel_admin", is_active=False)

        if search.lower() == "disable":
            owners = User.objects.filter(role="hotel_admin", is_active=True)

    allowed_sort_fields = {
        "id": "id",
        "name": "first_name",
        "email": "email",
        "status": "is_active",
        "action": "is_active",
    }

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    prefix = "-" if sort_order == "desc" else ""

    if sort_by == "name":
        owners = owners.order_by(f"{prefix}first_name", f"{prefix}last_name")
    else:
        owners = owners.order_by(f"{prefix}{allowed_sort_fields[sort_by]}")

    return render(request, "superadmin/owners.html", {
        "owners": owners,
        "search": search,
        "sort_by": sort_by,
        "sort_order": sort_order,
    })
    
# APPROVE OWNER
@login_required(login_url="/super/")
def approve_owner(request, user_id):
    owner = get_object_or_404(User, id=user_id)
    owner.is_active = True
    owner.save()
    return redirect("/super/owners/")

# DISABLE OWNER
@login_required(login_url="/super/")
def disable_owner(request, user_id):
    owner = get_object_or_404(User, id=user_id)
    owner.is_active = False
    owner.save()
    return redirect("/super/owners/")

# ENABLE OWNER
@login_required(login_url="/super/")
def enable_owner(request, user_id):
    owner = get_object_or_404(request, id=user_id)
    owner.is_active = True
    owner.save()
    return redirect("/super/owners/")

# =================  Hotel Management =================
@login_required(login_url="/super/")
def hotels_approve(request):
    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")
    search = request.GET.get("search", "").strip()
    tab = request.GET.get("tab", "live")
    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")
    hotels = Hotel.objects.all()

    # ---------- SEARCH FILTER ----------
    if search:
        # direct ID search
        if search.isdigit():
            hotels = hotels.filter(id=int(search))
        else:
            hotels = hotels.filter(
                Q(hotel_name__icontains=search) |
                Q(city__icontains=search) |
                Q(owner__username__icontains=search) |
                Q(owner__email__icontains=search)
            )

    # ---------- GLOBAL COUNTS ----------
    pending_count  = Hotel.objects.filter(status="PENDING").count()
    live_count     = Hotel.objects.filter(status="LIVE").count()
    rejected_count = Hotel.objects.filter(status="REJECTED").count()

    # ---------- UPDATE REQUESTS ----------
    pending_requests = ChangeRequest.objects.filter(
        status="PENDING"
    )

    hotel_sort_fields = {
        "id": "id",
        "hotel": "hotel_name",
        "city": "city",
        "owner": "owner__username",
        "status": "status",
        "reason": "verification_remarks",
    }
    update_sort_fields = {
        "hotel": "hotel__hotel_name",
        "category": "category",
        "requested_at": "requested_at",
    }

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"
    prefix = "-" if sort_order == "desc" else ""

    if tab == "updates":
        if sort_by not in update_sort_fields:
            sort_by = "requested_at"
            sort_order = "desc"
            prefix = "-"
        pending_requests = pending_requests.order_by(
            f"{prefix}{update_sort_fields[sort_by]}",
            f"{prefix}id",
        )
        hotels = hotels.order_by("id")
    else:
        if sort_by not in hotel_sort_fields:
            sort_by = "id"
        hotels = hotels.order_by(f"{prefix}{hotel_sort_fields[sort_by]}", f"{prefix}id")
        pending_requests = pending_requests.order_by("-requested_at")

    return render(request, "superadmin/hotels.html", {
        "hotels": hotels,
        "search": search,
        "tab": tab,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "pending_count": pending_count,
        "live_count": live_count,
        "rejected_count": rejected_count,
        "pending_requests": pending_requests
    })
    
@login_required(login_url="/super/")
def hotel_detail_view(request, hotel_id):
    """Full hotel detail for Super Admin review — shows all onboarding data."""
    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    hotel  = get_object_or_404(Hotel, id=hotel_id)
    images = HotelImage.objects.filter(hotel=hotel)
    rooms = RoomType.objects.filter(hotel=hotel)

    for r in rooms:
        if r.amenities:
            r.amenities_list = r.amenities
        else:
            r.amenities_list = []

    return render(request, "superadmin/hotel_detail.html", {
        "hotel":  hotel,
        "rooms":  rooms,
        "images": images,
    })

@login_required(login_url="/super/")
def approve_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # uniqueness check
    duplicate = Hotel.objects.filter(
        hotel_name__iexact=hotel.hotel_name,
        status="LIVE"
    ).exclude(id=hotel.id).exists()

    if duplicate:
        return HttpResponse("Another LIVE hotel with same name exists.")

    hotel.status = "LIVE"
    hotel.is_live = True
    hotel.verification_remarks = "Approved by Super Admin"
    hotel.save()

    return redirect("/super/hotels/")

@login_required(login_url="/super/")
def block_hotel(request, hotel_id):
    h = Hotel.objects.get(id=hotel_id)
    h.status = "blocked"
    h.save()
    return redirect("/super/hotels/")

# Reject hotel with reason mail
@login_required(login_url="/super/")
def reject_hotel(request, hotel_id):

    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        reason = request.POST.get("reason")

        hotel.status = "REJECTED"
        hotel.is_live = False
        hotel.verification_remarks = reason
        hotel.save()

        send_mail(
            "Hotel Rejected",
            f"Your hotel '{hotel.hotel_name}' was rejected.\nReason: {reason}",
            settings.EMAIL_HOST_USER,
            [hotel.owner.email],
            fail_silently=True,
        )

        return redirect("/super/hotels/")

    return render(request, "superadmin/reject_form.html", {"hotel": hotel})

#=================Booking manage=================
@login_required(login_url="/super/")
def bookings_manage(request):
    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")
    search = request.GET.get("search", "").replace(",", "").strip()
    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")

    bookings = Booking.objects.all()

    if search:
        if search.isdigit():
            bookings = bookings.filter(id=int(search))
        else:
            q = Q(hotel__hotel_name__icontains=search) | Q(user__email__icontains=search) | Q(booking_status__icontains=search) | Q(id__icontains=search)
            # Try to detect date formats
            date_formats = [
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
                "%Y/%m/%d",
                "%B %d %Y",
                "%b %d %Y",
                "%d %B %Y",
                "%d %b %Y",
            ]
            for fmt in date_formats:
                try:
                    parsed = datetime.strptime(search, fmt).date()
                    q |= Q(checkin_date=parsed)
                    q |= Q(checkout_date=parsed)
                    break
                except:
                    pass
            bookings = bookings.filter(q)

    allowed_sort_fields = {
        "id": "id",
        "hotel": "hotel__hotel_name",
        "guest": "user__email",
        "checkin": "checkin_date",
        "checkout": "checkout_date",
        "total_price": "total_price",
        "commission": "commission_amount",
    }

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    if sort_by == "commission":
        bookings = bookings.annotate(
            commission_amount=ExpressionWrapper(
                F("total_price") * Decimal("0.10"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )

    prefix = "-" if sort_order == "desc" else ""
    bookings = bookings.order_by(f"{prefix}{allowed_sort_fields[sort_by]}", f"{prefix}id")

    total_revenue = bookings.aggregate(Sum("total_price"))["total_price__sum"] or 0
    total_commission = total_revenue * Decimal("0.10")

    return render(request,"superadmin/bookings.html",{
        "bookings": bookings,
        "total_revenue": total_revenue,
        "total_commission": total_commission,
        "search": search,
        "sort_by": sort_by,
        "sort_order": sort_order,
    })

# ================= PAYMENTS DASHBOARD =================
@login_required(login_url="/super/")
def payments_dashboard(request):
    return render(request, "superadmin/payments_dashboard.html")

# GENERATE COMMISSION
@login_required(login_url="/super/")
def generate_commission(request):

    month_input = request.GET.get("month")
    

    if not month_input:
        return redirect("/super/payments/invoices/")

    if month_input:
        dt = datetime.strptime(month_input, "%Y-%m")
        month = dt.month
        year = dt.year
    else:
        today = date.today()
        month = today.month
        year = today.year

    hotels = Hotel.objects.filter(status="LIVE")

    for h in hotels:
        bookings = Booking.objects.filter(
            hotel=h,
            booking_status="confirmed",
            checkin_date__month=month,
            checkin_date__year=year
        )

        total_revenue = 0

        for b in bookings:
            nights = (b.checkout_date - b.checkin_date).days
            total_revenue += b.room.price_per_night * nights

        total_bookings = bookings.count()

        commission_percent = 10
        commission_amount = total_revenue * commission_percent / 100

        due_date = date.today() + timedelta(days=5)

        HotelCommission.objects.update_or_create(
            hotel=h,
            month=month,
            year=year,
            defaults={
                "total_bookings": total_bookings,
                "total_revenue": total_revenue,
                "commission_amount": commission_amount,
                "due_date": due_date,
                "status": "unpaid"
            }
        )
    return redirect("/super/payments/invoices/")

# VIEW INVOICES
@login_required(login_url="/super/")
def commissions(request):

    month_input = request.GET.get("month")  # e.g. "2026-02"
    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")
    today = date.today()

    if month_input:
        dt = datetime.strptime(month_input, "%Y-%m")
        month = dt.month
        year = dt.year

        invoices = HotelCommission.objects.filter(
            month=month,
            year=year
        ).order_by("id")
    else:
        invoices = HotelCommission.objects.all().order_by("id")

    # penalty update only on shown invoices
    for i in invoices:
        if i.status == "unpaid" and today > i.due_date:
            i.status = "overdue"
            i.penalty_amount = i.commission_amount * Decimal("0.05")
            i.save()

    allowed_sort_fields = {
        "id": "id",
        "hotel": "hotel__hotel_name",
        "commission": "commission_amount",
        "penalty": "penalty_amount",
        "total_revenue": "total_revenue",
        "status": "status",
        "due_date": "due_date",
        "action": "status",
        "month": "month",
        "total_pay": "total_payable_calc",
    }

    if sort_by not in allowed_sort_fields:
        sort_by = "id"

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    if sort_by == "total_pay":
        invoices = invoices.annotate(
            total_payable_calc=ExpressionWrapper(
                F("commission_amount") + F("penalty_amount"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )

    prefix = "-" if sort_order == "desc" else ""
    if sort_by == "month":
        invoices = invoices.order_by(f"{prefix}year", f"{prefix}month", f"{prefix}id")
    else:
        invoices = invoices.order_by(f"{prefix}{allowed_sort_fields[sort_by]}", f"{prefix}id")

    return render(request, "superadmin/commissions.html", {
        "data": invoices,
        "selected_month": month_input,
        "sort_by": sort_by,
        "sort_order": sort_order,
    })

# MARK PAID
@login_required(login_url="/super/")
def mark_paid(request, id):

    p = get_object_or_404(HotelCommission, id=id)
    p.status = "paid"
    p.penalty = 0
    p.save()

    return redirect("/super/payments/invoices/")

# SEND PAYMENT REMINDER
@login_required(login_url="/super/")
def send_payment_mail(request, id):

    p = HotelCommission.objects.get(id=id)

    send_mail(
        "Commission Payment Due",
        f"""
        Hotel: {p.hotel.hotel_name}
        Amount: ₹{p.commission_amount}
        Due date: {p.due_date}

        Please pay within 5 days.
        """,
        settings.EMAIL_HOST_USER,
        [p.hotel.owner.email],
        fail_silently=True,
    )

    return redirect("/super/payments/invoices/")

# ================= CUSTOMER MANAGE =================
@login_required(login_url="/super/")
def customers_manage(request):

    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    search = request.GET.get("search", "")
    sort_by = request.GET.get("sort_by", "id")
    sort_order = request.GET.get("sort_order", "asc")

    customers = User.objects.filter(role="customer")

    if search:
        if search.isdigit():
            customers = customers.filter(id=int(search))
        else:
            customers = customers.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        if search.lower() == "active":
            customers = customers.filter(is_active=True)

        if search.lower() in ["blacklist","blacklisted"]:
            customers = customers.filter(is_active=False)

    data = []

    for c in customers:
        total = Booking.objects.filter(user=c).count()

        # total booking search
        if search.isdigit():
            if str(total) != search:
                continue

        data.append({
            "obj": c,
            "total": total
        })

    if sort_order not in ["asc", "desc"]:
        sort_order = "asc"

    reverse = sort_order == "desc"

    if sort_by == "name":
        data = sorted(
            data,
            key=lambda d: ((d["obj"].first_name or "").lower(), (d["obj"].last_name or "").lower()),
            reverse=reverse,
        )
    elif sort_by == "email":
        data = sorted(data, key=lambda d: (d["obj"].email or "").lower(), reverse=reverse)
    elif sort_by == "total_bookings":
        data = sorted(data, key=lambda d: d["total"], reverse=reverse)
    elif sort_by == "status":
        data = sorted(data, key=lambda d: d["obj"].is_active, reverse=reverse)
    elif sort_by == "action":
        data = sorted(
            data,
            key=lambda d: "blacklist" if d["obj"].is_active else "unblock",
            reverse=reverse,
        )
    else:
        sort_by = "id"
        data = sorted(data, key=lambda d: d["obj"].id, reverse=reverse)

    return render(request, "superadmin/customers.html", {
        "data": data,
        "search": search,
        "sort_by": sort_by,
        "sort_order": sort_order,
    })
    
#Blacklist customer
@login_required(login_url="/super/")
def blacklist_customer(request, user_id):

    c = User.objects.get(id=user_id)
    c.is_active = False
    c.save()

    return redirect("/super/customers/")

#Unblock customer
@login_required(login_url="/super/")
def unblock_customer(request, user_id):

    c = User.objects.get(id=user_id)
    c.is_active = True
    c.save()

    return redirect("/super/customers/")

# ================= Review Moderate =================
@login_required(login_url="/super/")
def reviews_moderate(request):

    reviews = Review.objects.filter(status="delete_request")
    return render(request, "superadmin/reviews.html", {"reviews": reviews})

@login_required(login_url="/super/")
def approve_delete_review(request, id):

    r = get_object_or_404(Review, id=id)
    r.status = "deleted"
    r.save()
    return redirect("/super/reviews/")

@login_required(login_url="/super/")
def reject_delete_review(request, id):

    r = get_object_or_404(Review, id=id)
    r.status = "active"
    r.save()
    return redirect("/super/reviews/")

@login_required(login_url="/super/")
def mark_fake_review(request, id):

    r = get_object_or_404(Review, id=id)
    r.status = "fake"
    r.save()

    return redirect("/super/reviews/")

# ================= Change Request =================
@login_required(login_url="/super/")
def change_requests_list(request):

    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    pending_requests = ChangeRequest.objects.filter(status="PENDING").order_by("-requested_at")
    approved_requests = ChangeRequest.objects.filter(status="APPROVED").order_by("-requested_at")
    rejected_requests = ChangeRequest.objects.filter(status="REJECTED").order_by("-requested_at")

    context = {
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests
    }

    return render(request, "superadmin/hotels.html", context)

@login_required(login_url="/super/")
def approve_change_request(request, request_id):

    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    change_req = get_object_or_404(ChangeRequest, id=request_id)
    hotel = change_req.hotel

    # Apply requested changes to hotel
    for field, value in change_req.requested_data.items():
        if hasattr(hotel, field):
            setattr(hotel, field, value)

    hotel.save()

    # Update request status
    change_req.status = "APPROVED"
    change_req.reviewed_at = timezone.now()
    change_req.save()

    send_mail(
        "Hotel Update Approved",
        f"Your requested updates for '{hotel.hotel_name}' have been approved and are now live.",
        settings.EMAIL_HOST_USER,
        [hotel.owner.email],
        fail_silently=True,
    )

    return redirect("/super/hotels/")

@login_required(login_url="/super/")
def reject_change_request(request, request_id):

    if request.user.role != "super_admin":
        return HttpResponse("Unauthorized")

    change_req = get_object_or_404(ChangeRequest, id=request_id)

    if request.method == "POST":

        remarks = request.POST.get("remarks")

        change_req.status = "REJECTED"
        change_req.remarks = remarks
        change_req.reviewed_at = timezone.now()
        change_req.save()

        send_mail(
            "Hotel Update Rejected",
            f"Your requested updates for '{change_req.hotel.hotel_name}' were rejected.\nReason: {remarks}",
            settings.EMAIL_HOST_USER,
            [change_req.hotel.owner.email],
            fail_silently=True,
        )

        return redirect("/super/hotels/")

    return render(
        request,
        "superadmin/reject_change_form.html",
        {"change_req": change_req}
    )
    