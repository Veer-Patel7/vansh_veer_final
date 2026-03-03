from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookings.models import Booking
from .models import Hotel, RoomType, HotelImage, Offer, ChangeRequest
from .forms import HotelDeploymentForm, RoomTypeForm, HotelPolicyForm, HotelImageForm, OfferForm
from reviews.models import Review

from django.db import transaction

# --- 1. Property Identity (Unified Onboarding) ---
@login_required
def add_hotel(request):
    """Professional Multi-step Hotel Onboarding View"""
    if request.method == 'POST':
        form = HotelDeploymentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Save Hotel Base
                    hotel = form.save(commit=False)
                    hotel.owner = request.user
                    
                    # 2. Add Services (Step 2B)
                    services = request.POST.getlist('services')
                    hotel.services = services
                    hotel.save()

                    # 3. Save Hotel Policy (Step 2C) directly to Hotel model
                    hotel.check_in = request.POST.get('check_in', '14:00')
                    hotel.check_out = request.POST.get('check_out', '11:00')
                    hotel.cancellation_policy = request.POST.get('cancellation_rules', 'Standard Rules Apply')
                    hotel.save()

                    # 4. Save Dynamic Room Types (Step 2A)
                    room_idx = 1
                    while f'room_name_{room_idx}' in request.POST:
                        room_name = request.POST.get(f'room_name_{room_idx}')
                        room_class = request.POST.get(f'room_class_{room_idx}', 'STANDARD')
                        price = int(request.POST.get(f'room_price_{room_idx}', 0))
                        guests = int(request.POST.get(f'room_guests_{room_idx}', 2))
                        inventory = int(request.POST.get(f'room_count_{room_idx}', 1))
                        amenities_json = request.POST.get(f'room_amenities_{room_idx}', '[]')
                        
                        import json
                        try:
                            amenities = json.loads(amenities_json)
                        except:
                            amenities = []

                        RoomType.objects.create(
                            hotel=hotel,
                            room_category_name=room_name,
                            room_type=room_class.upper(),
                            price_per_night=price,
                            max_guests=guests,
                            total_rooms=inventory,
                            amenities=amenities
                        )
                        room_idx += 1

                    messages.success(request, f"Welcome ABOARD! {hotel.hotel_name} is now in review.")
                    return redirect('hotels:admin_dashboard_pro')
            except Exception as e:
                messages.error(request, f"Onboarding failed: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = HotelDeploymentForm()
    return render(request, 'hotels/add_hotel.html', {'form': form})

# --- 2. Room Inventory (Module 2) ---
@login_required
def create_room_type(request, hotel_id):
    """Hotel mein room categories (Standard/Deluxe) add karne ke liye"""
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            messages.success(request, f"{room.room_type} Category Added!")
            return redirect('hotels:hotel_dashboard', hotel_id=hotel.id)
    else:
        form = RoomTypeForm()
    return render(request, 'hotels/room_form.html', {'form': form, 'hotel': hotel})

# --- 3. Operational Policies (Module 3) ---
@login_required
def setup_policy(request, hotel_id):
    """Check-in/Check-out aur rules set karne ke liye"""
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    policy = hotel # Policy fields are now in the Hotel model
    
    if request.method == 'POST':
        form = HotelPolicyForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "Policies Updated!")
            return redirect('hotels:hotel_dashboard', hotel_id=hotel.id)
    else:
        form = HotelPolicyForm(instance=hotel)
    return render(request, 'hotels/policy_form.html', {'form': form, 'hotel': hotel})

# --- 4. Visual Assets / Gallery (Module 4) ---
@login_required
def upload_images(request, hotel_id):
    """Hotel ki photos gallery mein upload karne ke liye"""
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    if request.method == 'POST':
        images = request.FILES.getlist('images') # Multi-upload logic
        for img in images:
            HotelImage.objects.create(hotel=hotel, image_path=img)
        messages.success(request, f"{len(images)} Images Uploaded!")
        return redirect('hotels:hotel_dashboard', hotel_id=hotel.id)
    return render(request, 'hotels/upload_gallery.html', {'hotel': hotel})

# --- 5. Main Dashboard (The Controller) ---
@login_required
def hotel_dashboard(request, hotel_id):
    """Sare models ka data yahan calculate hota hai progress ke liye"""
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    
    # Logic for Completion Logic (Serializers wala formula yahan bhi kaam ayega)
    rooms = hotel.rooms.all()
    image_count = hotel.images.count()
    # Check if policy fields are filled (not default or empty)
    has_policy = bool(hotel.check_in and hotel.check_out and hotel.cancellation_policy)
    
    pending_requests = ChangeRequest.objects.filter(
        hotel=hotel,
        status='PENDING'
    ).values_list('category', flat=True)

    pending_categories = list(pending_requests)

    context = {
        'hotel': hotel,
        'rooms': rooms,
        'image_count': image_count,
        'has_rooms': rooms.exists(),
        'has_policy': has_policy,
        'pending_categories': pending_categories or [],
        # Progress Calculation
        'progress': (40 if rooms.exists() else 0) + (40 if image_count >= 5 else 0) + (20 if has_policy else 0)
    }
    return render(request, 'hotels/dashboard.html', context)




@login_required
def admin_dashboard_pro(request):
    """Executive Dashboard for Hotel Owners"""
    owned_hotels = Hotel.objects.filter(owner=request.user)
    primary_hotel = owned_hotels.first()
    
    # Recent reviews across all owned hotels
    recent_reviews = Review.objects.filter(hotel__in=owned_hotels).order_by('-created_at')[:5]
    
    # Stats Calculation
    from django.utils import timezone
    from django.db.models import Sum, Avg
    today = timezone.now().date()
    
    total_hotels = owned_hotels.count()
    bookings_today = Booking.objects.filter(hotel__in=owned_hotels, created_at__date=today).count()
    revenue_today = Booking.objects.filter(hotel__in=owned_hotels, created_at__date=today).aggregate(total=Sum('room__price_per_night'))['total'] or 0
    avg_rating = Review.objects.filter(hotel__in=owned_hotels).aggregate(avg=Avg('rating'))['avg'] or 5.0
    
    context = {
        'owned_hotels': owned_hotels,
        'primary_hotel_status': primary_hotel.status if primary_hotel else 'DRAFT',
        'primary_hotel_remarks': primary_hotel.verification_remarks if primary_hotel else '',
        'is_admin': request.user.role == 'ADMIN',
        'recent_reviews': recent_reviews,
        'total_hotels': total_hotels,
        'bookings_today': bookings_today,
        'revenue_today': f"₹{revenue_today:,}",
        'avg_rating': f"{avg_rating:.1f}"
    }
    return render(request, 'hotels/admin_dashboard_pro.html', context)

@login_required
def my_hotels(request):
    """List of all hotels owned by the current user"""
    owned_hotels = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotels/my_hotels.html', {'owned_hotels': owned_hotels})

# --- Offers Management ---

@login_required
def offers_view(request):
    owned_hotels = Hotel.objects.filter(owner=request.user)
    offers = Offer.objects.filter(hotel__in=owned_hotels)
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        offers = offers.filter(status=status_filter.upper())

    # Real Stats
    from django.db.models import Sum
    total_redemptions = offers.aggregate(total=Sum('redemption_count'))['total'] or 0
    offer_revenue = Booking.objects.filter(applied_offer__in=offers).aggregate(total=Sum('total_price'))['total'] or 0
    active_campaigns = offers.filter(status='LIVE').count()

    stats = {
        'total_redemptions': total_redemptions,
        'offer_revenue': offer_revenue,
        'conversion_lift': 12.5,
        'active_campaigns': active_campaigns
    }

    return render(request, 'hotels/offers.html', {'offers': offers, 'stats': stats})

@login_required
def create_offer(request):
    owned_hotels = Hotel.objects.filter(owner=request.user)
    room_types = RoomType.objects.filter(hotel__in=owned_hotels)
    
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            messages.success(request, "Offer created successfully!")
            return redirect('hotels:offers')
    else:
        form = OfferForm()
    
    context = {
        'form': form,
        'owned_hotels': owned_hotels,
        'room_types': room_types,
        'mode': 'create'
    }
    return render(request, 'hotels/add_offer.html', context)

@login_required
def edit_offer(request, offer_id):
    owned_hotels = Hotel.objects.filter(owner=request.user)
    room_types = RoomType.objects.filter(hotel__in=owned_hotels)
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    
    if request.method == 'POST':
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Offer updated!")
            return redirect('hotels:offers')
    else:
        form = OfferForm(instance=offer)
    
    context = {
        'form': form,
        'offer': offer,
        'owned_hotels': owned_hotels,
        'room_types': room_types,
        'mode': 'edit'
    }
    return render(request, 'hotels/add_offer.html', context)

@login_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    offer.delete()
    messages.success(request, "Offer terminated.")
    return redirect('hotels:offers')

@login_required
def submit_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    offer.status = 'PENDING'
    offer.save()
    messages.success(request, "Offer submitted for approval.")
    return redirect('hotels:offers')

# --- Admin Verifications ---

@login_required
def admin_verify_list(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()
    pending_hotels = Hotel.objects.filter(status='PENDING')
    return render(request, 'hotels/admin/verify_list.html', {'pending_hotels': pending_hotels})

@login_required
def admin_approve_hotel(request, hotel_id):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.status = 'LIVE'
    hotel.is_live = True
    hotel.save()
    messages.success(request, f"{hotel.hotel_name} is now LIVE!")
    return redirect('hotels:admin_verify_list')

@login_required
def admin_offer_list(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()
    pending_offers = Offer.objects.filter(status='PENDING')
    return render(request, 'hotels/admin/offer_review_list.html', {'pending_offers': pending_offers})

@login_required
def admin_review_offer(request, offer_id):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden()
    offer = get_object_or_404(Offer, id=offer_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            offer.status = 'APPROVED'
            messages.success(request, "Offer approved!")
        else:
            offer.status = 'REJECTED'
            offer.rejection_reason = request.POST.get('rejection_reason')
            messages.warning(request, "Offer rejected.")
        offer.save()
        return redirect('hotels:admin_offer_list')
    return render(request, 'hotels/admin/offer_review_detail.html', {'offer': offer})

# --- Bookings, Insights, etc. ---

@login_required
def bookings_view(request):
    owned_hotels = Hotel.objects.filter(owner=request.user)
    bookings = bookings.objects.filter(hotel__in=owned_hotels).order_by('-created_at')
    return render(request, 'hotels/bookings.html', {'bookings': bookings})

@login_required
def insights_view(request):
    return render(request, 'hotels/insights.html')

@login_required(login_url="/hotel/login/")
def hotel_reviews(request):

    reviews = Review.objects.filter(hotel__owner=request.user)

    return render(request, "hotels/reviews.html", {"reviews": reviews})


@login_required(login_url="/hotel/login/")
def request_delete_review(request, id):

    r = Review.objects.get(id=id)

    if r.hotel.owner != request.user:
        return HttpResponse("Unauthorized")

    r.status = "delete_request"
    r.save()

    return redirect("/hotel/reviews/")

@login_required
def settings_view(request):
    return render(request, 'hotels/settings.html')

# --- Property Edit Workflow ---

@login_required
def property_edit_detail(request, hotel_id, category):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    # Simple JSON data response for the modal
    data = {
        'hotel_name': hotel.hotel_name,
        'hotel_type': hotel.hotel_type,
        'description': hotel.description,
        'city': hotel.city,
        'address': hotel.address,
    }
    return JsonResponse(data)

@login_required
def submit_edit_request(request, hotel_id, category):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    if request.method == 'POST':
        import json
        requested_data = json.loads(request.body)
        ChangeRequest.objects.create(
            hotel=hotel,
            category=category.upper(),
            requested_data=requested_data,
            status='PENDING'
        )
        return JsonResponse({'status': 'success', 'message': 'Request submitted!'})
    return JsonResponse({'status': 'error'}, status=400)

