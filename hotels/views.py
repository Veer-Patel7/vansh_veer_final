import logging
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import hotel_admin_required, super_admin_required
from .models import Hotel, RoomPhoto, RoomType, HotelImage, Offer, ChangeRequest, LocationHistory
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import HotelDeploymentForm, RoomTypeForm, HotelPolicyForm, OfferForm
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from bookings.models import Booking
from reviews.models import Review
from rest_framework.decorators import action 
from django.views.decorators.http import require_POST
from django.db import transaction, models
from django.db.models import Avg, Count, Sum
from decimal import Decimal
from .serializers import (
    HotelSerializer, RoomTypeSerializer, 
    HotelImageSerializer
)


logger = logging.getLogger('hotelpro')

HOTEL_SERVICE_CHOICES = [
    ('Wifi', 'High-speed WiFi'),
    ('Parking', 'Free Parking'),
    ('Pool', 'Swimming Pool'),
    ('Spa', 'Luxury Spa'),
    ('Gym', 'Fitness Center'),
    ('Restaurant', 'Fine Dining'),
    ('Bar', 'Premium Bar'),
    ('Laundry', 'Laundry Service'),
    ('Airport', 'Airport Transfer'),
    ('Conference', 'Conference Room'),
    ('Ev', 'EV Charging'),
    ('Pet', 'Pet Friendly'),
]



# --- 1. Property Identity (Unified Onboarding) ---

@hotel_admin_required
def add_hotel(request):

    if request.method == 'POST':

        post_data = request.POST.copy()

        # Fix lat lng rounding
        for field in ['lat', 'lng']:
            val = post_data.get(field)
            if val:
                try:
                    post_data[field] = str(round(float(val), 10))
                except (ValueError, TypeError):
                    pass

        form = HotelDeploymentForm(post_data, request.FILES)

        if form.is_valid():

            cleaned = form.cleaned_data

            # SAFE STRIP (Fix NoneType error)
            hotel_name = (cleaned.get('hotel_name') or "").strip()
            city = (cleaned.get('city') or "").strip()
            state = (cleaned.get('state') or "").strip()
            address = (cleaned.get('address') or "").strip()

            # Check duplicate hotel
            existing_hotel = Hotel.objects.filter(
                hotel_name__iexact=hotel_name,
                city__iexact=city,
                state__iexact=state,
                address__iexact=address
            ).exclude(status='REJECTED').first()

            if existing_hotel:
                messages.error(
                    request,
                    "A hotel with the same name and location already exists."
                )
                return render(request, 'hotels/add_hotel.html', {'form': form})

            try:
                with transaction.atomic():

                    hotel = form.save(commit=False)
                    hotel.owner = request.user

                    services = request.POST.getlist('services')
                    hotel.services = services
                    hotel.save()

                    total_inventory = 0
                    room_idx = 1

                    while f'room_name_{room_idx}' in request.POST:

                        room_name = request.POST.get(f'room_name_{room_idx}')
                        room_type = request.POST.get(f'room_type_{room_idx}', 'STANDARD')

                        try:
                            price_str = request.POST.get(f'room_price_{room_idx}', '0').replace(',', '')
                            price = int(float(price_str))
                            guests = int(request.POST.get(f'room_guests_{room_idx}', '2') or '2')
                            inventory = int(request.POST.get(f'room_count_{room_idx}', '1') or '1')
                        except (ValueError, TypeError):
                            price, guests, inventory = 0, 2, 1

                        amenities_json = request.POST.get(f'room_amenities_{room_idx}', '[]')
                        try:
                            amenities = json.loads(amenities_json)
                        except:
                            amenities = []

                        room = RoomType.objects.create(
                            hotel=hotel,
                            name=room_name,
                            room_type=room_type.upper(),
                            price_per_night=price,
                            max_guest=guests,
                            total_rooms=inventory,
                            amenities=amenities
                        )

                        room_photos = request.FILES.getlist(f'room_photos_{room_idx}')
                        if room_photos:
                            room.room_image = room_photos[0]
                            room.save()

                        total_inventory += inventory
                        room_idx += 1

                    # Property Images
                    property_images = request.FILES.getlist('property_images')

                    for img in property_images:
                        HotelImage.objects.create(
                            hotel=hotel,
                            image_path=img
                        )

                    hotel.total_rooms = total_inventory
                    hotel.submitted_at = timezone.now()
                    hotel.status = 'PENDING'
                    hotel.save()

                    messages.success(
                        request,
                        f"{hotel.hotel_name} is now in verification queue."
                    )

                    return redirect('hotels:admin_dashboard_pro')

            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")

        else:
            messages.error(request, "Please check the highlighted fields.")

    else:
        form = HotelDeploymentForm()

    return render(request, 'hotels/add_hotel.html', {'form': form})

@hotel_admin_required
def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    if request.method == 'POST':
        try:
            # ==============================
            # 1. BASIC DETAILS
            # ==============================
            hotel.hotel_name = (request.POST.get('hotel_name') or hotel.hotel_name or "").strip()
            hotel.hotel_type = request.POST.get('hotel_type') or hotel.hotel_type

            hotel.address = (request.POST.get('address') or hotel.address or "").strip()
            hotel.city = (request.POST.get('city') or hotel.city or "").strip()
            hotel.state = (request.POST.get('state') or hotel.state or "").strip()
            hotel.pincode = (request.POST.get('pincode') or hotel.pincode or "").strip()

            hotel.contact_number = (request.POST.get('contact_number') or hotel.contact_number or "").strip()
            hotel.website = (request.POST.get('website') or hotel.website or "").strip()
            hotel.narrative = (request.POST.get('hotel_narrative') or hotel.narrative or "").strip()

            # ==============================
            # 2. LOCATION
            # ==============================
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')

            if lat:
                try:
                    hotel.lat = float(lat)
                except:
                    pass

            if lng:
                try:
                    hotel.lng = float(lng)
                except:
                    pass

            # ==============================
            # 3. OPERATIONS
            # ==============================
            hotel.check_in = request.POST.get('check_in') or hotel.check_in
            hotel.check_out = request.POST.get('check_out') or hotel.check_out
            hotel.cancellation_policy = request.POST.get('cancellation_policy') or hotel.cancellation_policy

            try:
                hotel.star_rating = float(request.POST.get('star_rating') or hotel.star_rating)
            except:
                pass

            # ==============================
            # 4. SERVICES (JSON)
            # ==============================
            try:
                hotel.services = json.loads(request.POST.get('services', '[]'))
            except:
                hotel.services = []

            # ==============================
            # 5. COMPLIANCE
            # ==============================
            hotel.id_type = request.POST.get('id_type') or hotel.id_type
            hotel.id_number = (request.POST.get('id_number') or hotel.id_number or "").strip()
            hotel.govt_reg_number = (request.POST.get('govt_reg_number') or hotel.govt_reg_number or "").strip()
            hotel.gst_number = (request.POST.get('gst_number') or hotel.gst_number or "").strip()

            if request.FILES.get('doc_mandatory'):
                hotel.doc_mandatory = request.FILES.get('doc_mandatory')
            if request.FILES.get('doc_certificate'):
                hotel.doc_certificate = request.FILES.get('doc_certificate')
            if request.FILES.get('doc_gst'):
                hotel.doc_gst = request.FILES.get('doc_gst')
            hotel.save()

            # ==============================
            # 6. ROOMS UPDATE
            # ==============================
            processed_room_ids = []

            for key in request.POST.keys():
                if key.startswith('room_name_'):
                    idx = key.replace('room_name_', '')
                    name = request.POST.get(f'room_name_{idx}')
                    if not name:
                        continue
                    room_id = request.POST.get(f'room_id_{idx}')
                    try:
                        price = float(request.POST.get(f'room_price_{idx}', 0))
                        guests = int(request.POST.get(f'room_guests_{idx}', 2))
                        count = int(request.POST.get(f'room_count_{idx}', 1))
                    except:
                        price, guests, count = 0, 2, 1
                    room_type = request.POST.get(f'room_type_{idx}', 'STANDARD')
                    try:
                        amenities = json.loads(request.POST.get(f'room_amenities_{idx}', '[]'))
                    except:
                        amenities = []

                    # UPDATE
                    if room_id:
                        room = get_object_or_404(RoomType, id=room_id, hotel=hotel)
                        room.name = name
                        room.room_type = room_type
                        room.max_guest = guests
                        room.price_per_night = price
                        room.total_rooms = count
                        room.amenities = amenities
                        room.save()

                    # CREATE
                    else:
                        room = RoomType.objects.create(
                            hotel=hotel,
                            name=name,
                            room_type=room_type,
                            max_guest=guests,
                            price_per_night=price,
                            total_rooms=count,
                            amenities=amenities
                        )
                    processed_room_ids.append(room.id)
                    # ROOM IMAGES
                    files = request.FILES.getlist(f'room_photos_{idx}')
                    for f in files:
                        RoomPhoto.objects.create(room=room, media_file=f)
            # DELETE OLD ROOMS
            if processed_room_ids:
                hotel.rooms.exclude(id__in=processed_room_ids).delete()

            # ==============================
            # 7. GALLERY
            # ==============================
            gallery_files = request.FILES.getlist('property_images')
            for f in gallery_files:
                HotelImage.objects.create(hotel=hotel, image_path=f)
            messages.success(request, f"{hotel.hotel_name} updated successfully")
            return redirect('hotels:my_hotels')
        except Exception as e:
            logger.error(f"[Edit Hotel Error] {str(e)}")
            messages.error(request, f"Error: {str(e)}")
    rooms = hotel.rooms.all().prefetch_related('photos')
    gallery = hotel.images.all()

    return render(request, 'hotels/edit_hotel.html', {
        'hotel': hotel,
        'rooms': rooms,
        'gallery': gallery,
        'service_choices': HOTEL_SERVICE_CHOICES,
        'is_edit': True
    })

@hotel_admin_required
@require_POST
def delete_hotel(request, hotel_id):
    """
    Elite Deletion Protocol:
    1. Unverified properties (INCOMPLETE, PENDING, REJECTED) are removed instantly.
    2. Verified/Approved properties are put into DELETION_PENDING for audit.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    
    if hotel.can_delete_directly:
        name = hotel.hotel_name
        hotel.delete()
        messages.warning(request, f"Property '{name}' has been completely removed from your portfolio.")
    else:
        # Professional Decommissioning Path
        hotel.status = 'DELETION_REQ'
        hotel.save()
        messages.info(
            request, 
            f"Deletion request for '{hotel.hotel_name}' initiated. "
            "Our audit team will review and decommission the property within 24-48 business hours."
        )
    return redirect('hotels:my_hotels')

@login_required
def my_hotels(request):

    hotels = (
        Hotel.objects
        .filter(owner=request.user)
        .annotate(
            room_count=Count("rooms", distinct=True),
            booking_count=Count("app_hotel_bookings", distinct=True)
        )
    )

    context = {
        "hotels": hotels,
        "live_count": hotels.filter(is_live=True).count(),
        "audit_count": hotels.filter(status="PENDING").count(),
    }

    return render(request, "hotels/my_hotels.html", context)

# --- 2. Room Inventory (Module 2) ---
@hotel_admin_required
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

#------room management----------
@hotel_admin_required
def add_room(request, hotel_id=None, room_id=None):
    """
    Add or Edit a room category with media handling.
    """

    hotels = Hotel.objects.filter(owner=request.user)

    hotel = None

    # URL se hotel
    if hotel_id:
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    # POST se hotel override 
    if request.method == "POST":
        hotel_id_post = request.POST.get("hotel_id")

        if hotel_id_post:
            hotel = get_object_or_404(Hotel, id=hotel_id_post, owner=request.user)

    room = None
    if room_id and hotel:
        room = get_object_or_404(RoomType, id=room_id, hotel=hotel)

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            room_type = request.POST.get("room_type", "STANDARD")
            max_guest = int(request.POST.get("max_guest", 2))
            base_price = float(request.POST.get("base_price", 0))
            inventory = int(request.POST.get("inventory_count", 1))

            amenities_data = request.POST.get("amenities", "[]")

            try:
                amenities_list = json.loads(amenities_data)
            except:
                amenities_list = []

            # agar hotel nahi mila
            if not hotel:
                messages.error(request, "Please select a hotel first.")
                return redirect("hotels:manage_rooms")

            # ===== EDIT =====
            if room:
                room.name = name
                room.room_type = room_type
                room.max_guest = max_guest
                room.price_per_night = base_price
                room.total_rooms = inventory
                room.amenities = amenities_list
                room.save()

                messages.success(request, f"Room '{name}' updated successfully.")

            # ===== CREATE =====
            else:
                room = RoomType.objects.create(
                    hotel=hotel,
                    name=name,
                    room_type=room_type,
                    max_guest=max_guest,
                    price_per_night=base_price,
                    total_rooms=inventory,
                    amenities=amenities_list
                )

                messages.success(request, f"New Room '{name}' created successfully.")

            # ===== PHOTOS =====
            room_photos = request.FILES.getlist("room_photos")

            for photo in room_photos:
                RoomPhoto.objects.create(
                    room=room,
                    media_file=photo
                )

            return redirect("hotels:manage_rooms_hotel", hotel_id=hotel.id)

        except Exception as e:
            print("ERROR:", e)  #debug
            messages.error(request, f"Error: {str(e)}")

    return render(request, "hotels/add_room.html", {
        "hotel": hotel,
        "hotels": hotels,
        "room": room
    })
    
@hotel_admin_required
def manage_rooms(request, hotel_id=None):

    hotels = Hotel.objects.filter(owner=request.user)

    # agar hotel_id diya hai toh specific hotel
    if hotel_id:
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    else:
        hotel = None

    rooms = []
    if hotel:
        rooms = RoomType.objects.filter(hotel=hotel).prefetch_related('photos')

    return render(request, 'hotels/rooms.html', {
        'hotel': hotel,      # selected hotel
        'hotels': hotels,    # dropdown ke liye
        'rooms': rooms
    })

@hotel_admin_required
@require_POST
def delete_room(request, room_id):
    """Delete a room category."""
    hotel = Hotel.objects.filter(owner=request.user).first()
    room = get_object_or_404(RoomType, id=room_id, hotel=hotel)
    room.delete()
    messages.warning(request, f"Room '{room.name}' has been removed.")
    return redirect('hotels:manage_rooms')

# --- 3. Operational Policies (Module 3) ---
@hotel_admin_required
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
@hotel_admin_required
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
@hotel_admin_required
def hotel_dashboard(request, hotel_id=None):

    if hotel_id:
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    else:
        hotel = Hotel.objects.filter(owner=request.user).order_by('-created_at').first()

    if not hotel:
        return redirect('hotels:hotelregister')

    # ---------- ONBOARDING MODE ----------
    if not hotel.is_live:

        completed_score = 0
        total_score = 4
        pending_categories = []

        if hotel.onboarding_step > 1:
            completed_score += 1
        else:
            pending_categories.append('IDENTITY')

        if hotel.onboarding_step > 2:
            completed_score += 1
        else:
            pending_categories.append('OPS')

        has_rooms = hotel.rooms.exists()
        if has_rooms:
            completed_score += 0.5
        else:
            pending_categories.append('INVENTORY')

        image_count = hotel.images.count()
        if image_count >= 5:
            completed_score += 0.5
        else:
            pending_categories.append('GALLERY')

        progress_percentage = (completed_score / total_score) * 100

        rooms = hotel.rooms.all()
        gallery = hotel.images.all().order_by('-uploaded_at')

        return render(request, 'hotels/dashboard.html', {
            'hotel': hotel,
            'progress': int(progress_percentage),
            'pending_categories': pending_categories,
            'has_rooms': has_rooms,
            'rooms': rooms,
            'gallery': gallery,
            'image_count': image_count,
            'has_policy': bool(hotel.cancellation_policy),
        })

    # ---------- LIVE DASHBOARD ----------
    today = timezone.now().date()

    stats = {
        'total_bookings': hotel.app_hotel_bookings.count(),

        'active_offers': hotel.offers.filter(status="LIVE").count(),

        'avg_rating': hotel.app_reviews.aggregate(
            Avg('rating')
        )['rating__avg'] or 0.0,

        'recent_bookings': hotel.app_hotel_bookings.order_by('-created_at')[:5],

        'revenue_today': hotel.app_hotel_bookings.filter(
            booking_status='confirmed',
            created_at__date=today
        ).aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0,
    }

    rooms = hotel.rooms.all()

    return render(request, 'hotels/admin_dashboard_pro.html', {
        'hotel': hotel,
        'stats': stats,
        'rooms': rooms,
    })
@hotel_admin_required
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
    revenue_today = Booking.objects.filter(hotel__in=owned_hotels, created_at__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    avg_rating = Review.objects.filter(hotel__in=owned_hotels).aggregate(avg=Avg('rating'))['avg'] or 5.0
    
    context = {
        'owned_hotels': owned_hotels,
        'primary_hotel_status': primary_hotel.status if primary_hotel else 'DRAFT',
        'primary_hotel_remarks': primary_hotel.verification_remarks if primary_hotel else '',
        'is_admin': request.user.is_super_admin,
        'recent_reviews': recent_reviews,
        'total_hotels': total_hotels,
        'bookings_today': bookings_today,
        'revenue_today': f"₹{revenue_today:,}",
        'avg_rating': f"{avg_rating:.1f}"
    }
    return render(request, 'hotels/admin_dashboard_pro.html', context)

# --- Offers Management ---
@hotel_admin_required
def offers_view(request):
    """
    Manage Hotel Offers and Discounts Portfolio.
    """
    user_hotels = Hotel.objects.filter(owner=request.user)
    if not user_hotels.exists():
        return redirect('hotels:hotelregister')
        
    # Dynamic portfolio filtering
    offers_list = Offer.objects.filter(hotel__in=user_hotels).distinct().order_by('-created_at')
    
    # Professional Analytics (Aggregated)
    total_count = offers_list.count()
    active_count = offers_list.filter(status="LIVE").count()
    
    avg_redemption = 0

    if total_count > 0:
        total_redemptions = offers_list.aggregate(Sum('redemption_count'))['redemption_count__sum'] or 0
        avg_redemption = total_redemptions / total_count

    total_revenue = Booking.objects.filter(applied_offer__in=offers_list).aggregate(total=Sum('total_price'))['total'] or 0

    stats = {
        'active_offers': active_count,
        'draft_offers': total_count - active_count,
        'total_offers': total_count,
        'avg_discount': offers_list.aggregate(Avg('discount_value'))['discount_value__avg'] or 0,
        'avg_redemption': avg_redemption,
        'total_revenue': total_revenue,
    }

    # Templates Gallery Data
    templates = [
        {'id': 'early_bird', 'name': 'Early Bird Special', 'discount': 25, 'icon': 'fa-clock', 'category': 'PRICE', 'label': 'Advance Booking'},
        {'id': 'last_minute', 'name': 'Last Minute Deal', 'discount': 40, 'icon': 'fa-bolt', 'category': 'PRICE', 'label': 'Inventory Clearance'},
        {'id': 'fb_experience', 'name': 'Gourmet Stay', 'discount': 15, 'icon': 'fa-utensils', 'category': 'FB', 'label': 'F&B Bundle'},
        {'id': 'wellness', 'name': 'Wellness Retreat', 'discount': 20, 'icon': 'fa-spa', 'category': 'EXPERIENCE', 'label': 'Experience'},
    ]
    
    # Prepare JSON data for the calendar engine
    offers_json = []
    for o in offers_list:
        offers_json.append({
            'name': o.name,
            'activation_date': o.activation_date.strftime('%Y-%m-%d') if o.activation_date else None,
            'expiration_date': o.expiration_date.strftime('%Y-%m-%d') if o.expiration_date else None,
            'is_live': o.status == "LIVE"
        })

    return render(request, 'hotels/offers.html', {
        'offers': offers_list, 
        'offers_json': offers_json,
        'user_hotels': user_hotels,
        'hotel': user_hotels.first(),
        'stats': stats,
        'templates': templates
    })
    
@hotel_admin_required
def add_offer(request, offer_id=None):
    """
    Create or Edit Hotel Offers.
    Handles precise targeting across multiple properties and specific room categories.
    """
    user_hotels = Hotel.objects.filter(owner=request.user)
    if not user_hotels.exists(): 
        return redirect('hotels:hotelregister')
        
    offer = None
    if offer_id:
        # Secure retrieval: must be owned by user through at least one targeted hotel
        offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
        
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            if offer:
                code = offer.code
            else:
                import uuid
                code = uuid.uuid4().hex[:8].upper()
            
            # Elite field mapping
            category = request.POST.get('category', 'PRICE')
            promotion_type = request.POST.get('promo_type', 'PERCENT')
            discount = request.POST.get('discount_value', 0)
            min_nights = request.POST.get('min_nights_stay', 1)
            
            # Window mapping
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            
            # Professional date parsing
            activation_date = None
            expiration_date = None
            if start_date_str:
                activation_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                expiration_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            strategy = request.POST.get('strategy', 'DIRECT')
            limit = request.POST.get('usage_limit', -1)
            min_spend = request.POST.get('min_booking_amount', 0)
            max_disc = request.POST.get('max_discount_amount')
            description = request.POST.get('description', '')
            is_public = request.POST.get('is_public') == 'on'
            is_live = request.POST.get('is_live') == 'true'
            is_stackable = request.POST.get('is_stackable') == 'true'

            # Asset Orchestration
            hotel_ids = [hid for hid in request.POST.getlist('targeted_hotels') if hid.isdigit()]
            room_selection_mode = request.POST.get('room_selection_mode', 'ALL')
            
            if room_selection_mode == 'ALL':
                room_ids = list(RoomType.objects.filter(hotel_id__in=hotel_ids).values_list('id', flat=True))
            else:
                room_ids = [rid for rid in request.POST.getlist('targeted_rooms') if rid.isdigit()]

            if not hotel_ids:
                messages.warning(request, "Portfolio Alert: At least one property must be selected for activation.")
                return redirect('hotels:add_offer')

            perks = request.POST.get('perks', '')

            if offer:
                offer.name = name
                offer.code = code
                offer.strategy = strategy
                offer.category = category
                offer.promotion_type = promotion_type
                offer.min_nights_stay = min_nights
                offer.perks = perks
                offer.is_stackable = is_stackable
                offer.discount_percent = discount
                offer.activation_date = activation_date
                offer.expiration_date = expiration_date
                offer.usage_limit = limit
                offer.min_booking_amount = min_spend
                offer.max_discount_amount = max_disc if max_disc else None
                offer.description = description
                offer.is_public = is_public
                offer.is_live = is_live
                offer.status = 'ACTIVE' if is_live else 'DRAFT'
                offer.save()
            else:
                offer = Offer.objects.create(
                    name=name,
                    code=code,
                    strategy=strategy,
                    category=category,
                    promotion_type=promotion_type,
                    min_nights_stay=min_nights,
                    perks=perks,
                    is_stackable=is_stackable,
                    discount_percent=discount,
                    activation_date=activation_date,
                    expiration_date=expiration_date,
                    usage_limit=limit,
                    min_booking_amount=min_spend,
                    max_discount_amount=max_disc if max_disc else None,
                    description=description,
                    is_public=is_public,
                    is_live=is_live,
                    status='ACTIVE' if is_live else 'DRAFT',
                    scope='HOTEL'
                )

            # Sync M2M Relationships
            offer.targeted_hotels.set(Hotel.objects.filter(id__in=hotel_ids, owner=request.user))
            offer.targeted_rooms.set(RoomType.objects.filter(id__in=room_ids, hotel__owner=request.user))

            if is_stackable:
                combinable_ids = [cid for cid in request.POST.getlist('combinable_offers') if cid.isdigit()]
                offer.combinable_offers.set(Offer.objects.filter(id__in=combinable_ids, targeted_hotels__owner=request.user))
            else:
                offer.combinable_offers.clear()
            
            # Bonded Legacy Link (Unified Indexing)
            offer.hotel = offer.targeted_hotels.first()
            offer.save()

            status_msg = "Campaign activated across dossier." if is_live else "Strategic draft saved for future deployment."
            messages.success(request, f"Strategic Update: {status_msg}")
            return redirect('hotels:offers')
            
        except Exception as e:
            import traceback
            logger.error(f"[Strategic Failure] Offer Persistence Error: {str(e)}\n{traceback.format_exc()}")
            messages.error(request, f"Strategic Failure: {str(e)}")

    # Data for the "Elite" Selection Matrix
    all_rooms = RoomType.objects.filter(hotel__owner=request.user).select_related('hotel').prefetch_related('photos')
    
    # Pre-compute JSON for dynamic room rendering on frontend
    rooms_by_hotel = {}
    for room in all_rooms:
        hotel_id = str(room.hotel.id)
        if hotel_id not in rooms_by_hotel:
            rooms_by_hotel[hotel_id] = []
            
        photo = room.photos.first()
        photo_url = photo.media_file.url if photo else ""
        
        rooms_by_hotel[hotel_id].append({
            'id': str(room.id),
            'name': room.name,
            'room_type': room.room_type,
            'max_guest': room.max_guest,
            'price_per_night': float(room.price_per_night),
            'image': photo_url,
            'hotel_name': room.hotel.hotel_name
        })
        
    rooms_by_hotel_json = json.dumps(rooms_by_hotel)
    
    # Strategy Metadata for the refined Elite UI
    # Structure: (CODE, NAME, ICON, THEME, SUBTITLE, CATEGORY, PROMO_TYPE, DISCOUNT, MIN_NIGHTS)
    strategy_data = [
        ('SEASONAL', 'Summer Cycle', 'fa-sun', 'seasonal', '15% MAGNITUDE', 'PRICE', 'PERCENT', 15, 1),
        ('RETENTION', 'Extended Stay', 'fa-moon', 'stay', 'STAY 3+, PAY 2', 'STAY', 'BOGO', 0, 3),
        ('PREMIUM', 'Elite Retreat', 'fa-crown', 'experience', 'INCLUSION BUNDLE', 'EXPERIENCE', 'UPGRADE', 0, 1),
        ('GROWTH', 'Strategic Expansion', 'fa-chart-line', 'growth', 'VOLUME BOOST', 'PRICE', 'PERCENT', 20, 1),
        ('URGENCY', 'Flash Velocity', 'fa-fire-alt', 'urgency', 'LIMITED WINDOW', 'PRICE', 'FIXED', 1000, 1),
        ('LOYALTY', 'Elite Member', 'fa-award', 'loyalty', 'RETENTION MAGNET', 'PERKS', 'UPGRADE', 0, 1),
        ('ARCHITECT', 'Bespoke Offer', 'fa-pen-nib', 'custom', 'BUILD FROM ZERO', 'PRICE', 'PERCENT', 10, 1),
    ]
    
    # Professional Wizard Metadata
    default_perks = [
        'Complimentary Breakfast', 'Airport Transfer', 'Late Check-out', 
        'Early Check-in', 'Free High-Speed Wi-Fi', 'Spa Voucher', 
        'Dinner Credit', 'Room Upgrade', 'Welcome Drink'
    ]
    
    # Fetch existing offers for combinable options
    existing_offers = Offer.objects.filter(targeted_hotels__owner=request.user).distinct()
    if offer:
        existing_offers = existing_offers.exclude(id=offer.id)
    
    return render(request, 'hotels/add_offer.html', {
        'offer': offer,
        'user_hotels': user_hotels,
        'all_rooms': all_rooms,
        'rooms_by_hotel_json': rooms_by_hotel_json,
        'strategy_data': strategy_data,
        'default_perks': default_perks,
        'categories': Offer.CATEGORY_CHOICES,
        'promotion_types': Offer.PROMOTION_TYPE_CHOICES,
        'guest_segments': Offer.GUEST_SEGMENT_CHOICES,
        'existing_offers': existing_offers,
    })

@hotel_admin_required
def submit_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    offer.status = 'PENDING'
    offer.save()
    messages.success(request, "Offer submitted for approval.")
    return redirect('hotels:offers')

@login_required
def toggle_offer_status(request, offer_id):
    """
    Strategic Status Orchestration: Toggles an offer between LIVE and DRAFT.
    """
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Security: Ensure user owns either the bound hotel or at least one of the targeted hotels
    user_hotels = Hotel.objects.filter(owner=request.user)
    has_bound_access = offer.hotel and offer.hotel.owner == request.user
    has_targeted_access = offer.targeted_hotels.filter(owner=request.user).exists()
    
    if not (has_bound_access or has_targeted_access):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized Architecture Access'}, status=403)
    
    offer.is_live = not offer.is_live
    offer.save()
    
    status_label = "LIVE" if offer.is_live else "DRAFT"
    return JsonResponse({
        'status': 'success',
        'is_live': offer.is_live,
        'message': f'Offer is now {status_label}'
    })

@login_required
def delete_offer(request, offer_id):
    """
    Secure Decommissioning: Removes an offer from the portfolio archive.
    """
    offer = get_object_or_404(Offer, id=offer_id)
    
    # Security: Ensure user owns either the bound hotel or at least one of the targeted hotels
    user_hotels = Hotel.objects.filter(owner=request.user)
    has_bound_access = offer.hotel and offer.hotel.owner == request.user
    has_targeted_access = offer.targeted_hotels.filter(owner=request.user).exists()

    if not (has_bound_access or has_targeted_access):
        return JsonResponse({'status': 'error', 'message': 'Unauthorized Decommissioning Request'}, status=403)
    
    offer.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Strategy successfully removed from portfolio'
    })
    
def offer_usage_details(request, offer_id):

    try:
        offer = get_object_or_404(
            Offer,
            id=offer_id,
            hotel__owner=request.user
        )

        bookings = (
            Booking.objects
            .filter(applied_offer=offer)
            .select_related("room_category")
            .order_by("-created_at")
        )

        usage_data = []

        for b in bookings:
            usage_data.append({
                "guest_name": b.guest_name,
                "guest_email": b.guest_email,
                "guest_phone": b.guest_phone,
                "room_type": b.room_category.name if b.room_category else "Standard",
                "check_in": b.check_in.strftime("%b %d, %Y"),
                "check_out": b.check_out.strftime("%b %d, %Y"),
                "revenue": float(b.total_price),
                "reference": b.reference
            })

        return JsonResponse({
            "status": "success",
            "offer_name": offer.name,
            "usage_data": usage_data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

@hotel_admin_required
def offer_rooms_details(request, offer_id):

    try:
        offer = get_object_or_404(
            Offer,
            id=offer_id,
            hotel__owner=request.user
        )

        rooms = RoomType.objects.filter(
            hotel=offer.hotel,
            id__in=offer.room_categories
        ).prefetch_related("photos")

        rooms_data = []

        for room in rooms:

            first_photo = room.photos.first()
            photo_url = first_photo.media_file.url if first_photo else ""

            rooms_data.append({
                "name": room.name,
                "room_type": room.get_room_type_display(),
                "max_guests": room.max_guest,
                "price": float(room.price_per_night),
                "image": photo_url,
                "hotel_name": room.hotel.hotel_name
            })

        return JsonResponse({
            "status": "success",
            "offer_name": offer.name,
            "rooms": rooms_data
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)
        
# --- Admin Verifications ---

@super_admin_required
def admin_verify_list(request):
    pending_hotels = Hotel.objects.filter(status='PENDING')
    return render(request, 'hotels/admin/verify_list.html', {'pending_hotels': pending_hotels})

@super_admin_required
def admin_approve_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.status = 'LIVE'
    hotel.is_live = True
    hotel.save()
    messages.success(request, f"{hotel.hotel_name} is now LIVE!")
    return redirect('hotels:admin_verify_list')

@super_admin_required
def admin_offer_list(request):
    pending_offers = Offer.objects.filter(status='PENDING')
    return render(request, 'hotels/admin/offer_review_list.html', {'pending_offers': pending_offers})

@super_admin_required
def admin_review_offer(request, offer_id):
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

@hotel_admin_required
def bookings_view(request):
    bookings = Booking.objects.filter(hotel__owner=request.user)
    return render(request, "hotels/bookings.html", {"bookings": bookings})

@hotel_admin_required
def insights_view(request):
    return render(request, 'hotels/insights.html')

@hotel_admin_required
def reviews_view(request):
    owned_hotels = Hotel.objects.filter(owner=request.user)
    reviews = Review.objects.filter(hotel__in=owned_hotels).order_by('-created_at')
    
    from django.db.models import Avg
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 5.0
    total_reviews = reviews.count()
    
    context = {
        'reviews': reviews,
        'avg_rating': f"{avg_rating:.1f}",
        'total_reviews': total_reviews,
    }
    return render(request, 'hotels/reviews.html', context)

@hotel_admin_required
def settings_view(request):
    return render(request, 'hotels/settings.html')

# --- Property Edit Workflow ---

@hotel_admin_required
def property_edit_detail(request, hotel_id, category):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    category = category.upper()

    from .forms import HotelIdentityForm, RoomTypeForm

    # -------------------------------
    # IDENTITY EDIT
    # -------------------------------
    if category == "IDENTITY":

        if request.method == "POST":
            form = HotelIdentityForm(request.POST, instance=hotel)

            if form.is_valid():

                if ChangeRequest.objects.filter(
                    hotel=hotel,
                    category="IDENTITY",
                    status="PENDING"
                ).exists():
                    return JsonResponse({
                        "success": False,
                        "message": "Update request already pending approval."
                    })

                ChangeRequest.objects.create(
                    hotel=hotel,
                    category="IDENTITY",
                    requested_data=form.cleaned_data
                )

                if hotel.status == "REJECTED":
                    hotel.status = "PENDING"
                    hotel.save()

                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "errors": form.errors})

        form = HotelIdentityForm(instance=hotel)

        return render(request, "hotels/partials/edit_identity.html", {
            "form": form,
            "hotel": hotel,
            "category": category
        })


    # -------------------------------
    # INVENTORY (Rooms & Service)
    # -------------------------------
    elif category == "INVENTORY":

        if request.method == "POST":

            form = RoomTypeForm(request.POST)

            if form.is_valid():

                if ChangeRequest.objects.filter(
                    hotel=hotel,
                    category="INVENTORY",
                    status="PENDING"
                ).exists():
                    return JsonResponse({
                        "success": False,
                        "message": "Room update already pending approval."
                    })

                ChangeRequest.objects.create(
                    hotel=hotel,
                    category="INVENTORY",
                    requested_data=form.cleaned_data
                )

                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "errors": form.errors})

        form = RoomTypeForm()

        return render(request, "hotels/partials/edit_inventory.html", {
            "form": form,
            "hotel": hotel,
            "category": category
        })

    return HttpResponseForbidden("Invalid Category")

@hotel_admin_required
def submit_edit_request(request, hotel_id, category):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    if request.method == "POST":
        import json
        requested_data = json.loads(request.body)

        # Prevent duplicate pending request
        if ChangeRequest.objects.filter(
            hotel=hotel,
            category=category.upper(),
            status="PENDING"
        ).exists():
            return JsonResponse({
                "status": "error",
                "message": "Request already pending approval."
            })

        ChangeRequest.objects.create(
            hotel=hotel,
            category=category.upper(),
            requested_data=requested_data,
            status="PENDING"
        )

        return JsonResponse({
            "status": "success",
            "message": "Update request sent for approval."
        })

    return JsonResponse({"status": "error"}, status=400)


class HotelViewSet(viewsets.ModelViewSet):
    """
    The main API for Property Management.
    """
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticated]
    # MultiPartParser handles file/image uploads via API
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_queryset(self):
        """Owners only see their properties with optimized queries."""
        return Hotel.objects.filter(owner=self.request.user).prefetch_related(
            'rooms', 'images'
        )

    def perform_create(self, serializer):
        """Attach the logged-in user as the owner."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='request-approval')
    def request_approval(self, request, pk=None):
        """Business Logic: Request Go-Live status."""
        hotel = self.get_object()
        # Verify 100% completion before allowing approval request
        if hotel.rooms.count() == 0 or hotel.images.count() < 5:
            return Response(
                {"error": "Profile incomplete (Needs rooms and 5+ photos)."},
                status=status.HTTP_400_BAD_REQUEST
            )
        hotel.status = 'PENDING'
        hotel.save()
        return Response({'message': 'Approval request sent to admin.'})

class RoomTypeViewSet(viewsets.ModelViewSet):
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoomType.objects.filter(hotel__owner=self.request.user)

class GalleryViewSet(viewsets.ModelViewSet):
    """Handles Image Uploads & Deletions."""
    serializer_class = HotelImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_queryset(self):
        return HotelImage.objects.filter(hotel__owner=self.request.user)

# --- Phase 2: Location History API ---

@login_required
def get_location_history(request):
    """Fetch user's location history grouped by date (Recent vs Older)."""
    history_items = LocationHistory.objects.filter(user=request.user)
    
    # Optional filtering
    city_filter = request.GET.get('city')
    if city_filter and city_filter != 'All':
        history_items = history_items.filter(city__iexact=city_filter)

    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    recent = []
    older = []
    cities = set()

    for item in history_items:
        if item.city:
            cities.add(item.city)
            
        data = {
            'id': item.id,
            'lat': str(item.lat),
            'lng': str(item.lng),
            'formatted_address': item.formatted_address,
            'city': item.city,
            'location_name': item.location_name,
            'category': item.category,
            'rating': str(item.rating) if item.rating else None,
            'review_count': item.review_count,
            'image_reference': item.image_reference,
            'timestamp': item.timestamp.isoformat()
        }
        
        if item.timestamp >= three_days_ago:
            recent.append(data)
        else:
            older.append(data)

    return JsonResponse({
        'status': 'success',
        'cities': sorted(list(cities)),
        'recent': recent,
        'older': older
    })

@login_required
def add_location_history(request):
    """Add a newly verified location to the history."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Prevent duplicate inserts based on core coords
            existing = LocationHistory.objects.filter(
                user=request.user, 
                lat=data.get('lat'), 
                lng=data.get('lng')
            ).first()
            
            if not existing:
                LocationHistory.objects.create(
                    user=request.user,
                    lat=data.get('lat'),
                    lng=data.get('lng'),
                    formatted_address=data.get('address'),
                    city=data.get('city', ''),
                    location_name=data.get('locationName'),
                    category=data.get('category'),
                    rating=data.get('rating'),
                    review_count=data.get('reviewCount', 0),
                    image_reference=data.get('imageReference')
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@login_required
def bulk_action_location_history(request):
    """Handle bulk actions like delete on multiple history items."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            item_ids = data.get('ids', [])
            
            if action == 'delete' and item_ids:
                LocationHistory.objects.filter(user=request.user, id__in=item_ids).delete()
                
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@hotel_admin_required
def api_latest_booking(request):
    """API for real-time dashboard notifications."""

    hotel = Hotel.objects.filter(owner=request.user).first()

    if not hotel:
        return JsonResponse({'status': 'none'})

    latest = hotel.app_hotel_bookings.order_by('-created_at').first()

    if latest:
        # check booking created in last 60 seconds
        if (timezone.now() - latest.created_at).total_seconds() < 60:
            return JsonResponse({
                'status': 'new',
                'ref': latest.id,
                'guest': latest.user.email,
                'room': latest.room.name
            })

    return JsonResponse({'status': 'none'})
