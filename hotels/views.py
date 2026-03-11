import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import hotel_admin_required, super_admin_required
from .models import Hotel, RoomPhoto, RoomType, HotelImage, Offer, ChangeRequest, LocationHistory
import json
from django.utils import timezone
from datetime import timedelta
from .forms import HotelDeploymentForm, RoomTypeForm, HotelPolicyForm, OfferForm
from reviews.models import Review
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from bookings.models import Booking
from rest_framework.decorators import action
from .serializers import (
    HotelSerializer, RoomTypeSerializer, 
    HotelImageSerializer
) 
from django.views.decorators.http import require_POST
from django.db import transaction, models
from django.db.models import Avg, Count, Sum


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
                        room_class = request.POST.get(f'room_class_{room_idx}', 'STANDARD')

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
                            room_type=room_class.upper(),
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
    """
    Master Property Editor: Update Global Dossier.
    Handles updates for Identity, Inventory (Rooms), and Compliance.
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    
    if request.method == 'POST':
        print("POST KEYS:",request.POST.keys())
        try:
            # 1. Update Core Identity (Step 1 Fields)
            hotel.hotel_name = request.POST.get('hotel_name', hotel.hotel_name).strip()
            # hotel_type points to 'category' field in request data
            hotel_type = request.POST.get('hotel_type', '').strip()
            if hotel_type:
                hotel.hotel_type = hotel_type
                
            hotel.address = request.POST.get('address', hotel.address).strip()
            hotel.narrative = request.POST.get('hotel_narrative', hotel.narrative).strip()
            # Contact & Portfolio Intelligence
            hotel.contact_number = request.POST.get('contact_number', hotel.contact_number).strip()
            hotel.website = request.POST.get('website', hotel.website).strip()
            try:
                hotel.star_rating = float(request.POST.get('star_rating', hotel.star_rating))
            except (TypeError, ValueError):
                pass
            
            # Location Intelligence
            hotel.city = request.POST.get('city', hotel.city).strip()
            hotel.state = request.POST.get('state', hotel.state).strip()
            hotel.pincode = request.POST.get('pincode', hotel.pincode).strip()
            lat = request.POST.get('lat')
            lng = request.POST.get('lng')
            if lat: hotel.latitude = lat
            if lng: hotel.longitude = lng

            # Operational Rules (Step 2 Fields)
            hotel.check_in_time = request.POST.get('check_in', hotel.check_in_time)
            hotel.check_out_time = request.POST.get('check_out', hotel.check_out_time)
            hotel.cancellation_policy = request.POST.get('cancellation_policy', hotel.cancellation_policy)
            
            # Handle services list
            services_data = request.POST.get("services", "[]")
            try:
                hotel.services = json.loads(services_data)
            except:
                hotel.services = []
                
            # 3. Compliance Data (Step 3 Fields)
            hotel.id_type = request.POST.get('id_type', hotel.id_type)
            hotel.id_number = request.POST.get('id_number', hotel.id_number).strip()
            hotel.govt_reg_number = request.POST.get('govt_reg_number', hotel.govt_reg_number).strip()
            hotel.gst_number = request.POST.get('gst_number', hotel.gst_number).strip()
            
            # Handle Document Overwrites
            if request.FILES.get('doc_mandatory'): hotel.doc_mandatory = request.FILES.get('doc_mandatory')
            if request.FILES.get('doc_certificate'): hotel.doc_certificate = request.FILES.get('doc_certificate')
            if request.FILES.get('doc_gst'): hotel.doc_gst = request.FILES.get('doc_gst')
            
            hotel.save()

            # 4. Inventory Matrix Sync (Dynamic Rooms)
            # Find all room indices from the post data (matches room_name_X)
            new_room_indices = []
            for key in request.POST.keys():
                if key.startswith('room_name_'):
                    # The index might be a number or a timestamp from JS
                    idx = key.replace('room_name_', '')
                    if idx and idx != "__prefix__":
                        new_room_indices.append(idx)
            
            # Tracking existing room IDs to detect deletions
            processed_room_ids = []
            
            for idx in new_room_indices:
                room_id = request.POST.get(f'room_id_{idx}') # If it exists, it's an edit
                name = request.POST.get(f'room_name_{idx}')
                r_class = request.POST.get(f'room_class_{idx}', 'STANDARD')
                try:
                    guests = int(request.POST.get(f'room_guests_{idx}', 2))
                    price = float(request.POST.get(f'room_price_{idx}', 0))
                    count = int(request.POST.get(f'room_count_{idx}', 1))
                except:
                    guests, price, count = 2, 0, 1
                
                amenities_data = request.POST.get(f'room_amenities_{idx}', '[]')
                try: 
                    amenities_list = json.loads(amenities_data)
                    if not isinstance(amenities_list, list): amenities_list = []
                except: 
                    amenities_list = []

                if room_id: # Edit Existing
                    room = get_object_or_404(RoomType, id=room_id, hotel=hotel)
                    room.name = name
                    room.room_type = r_class
                    room.max_guest = guests
                    room.price_per_night = price
                    room.total_rooms = count
                    room.amenities = amenities_list
                    room.save()
                    processed_room_ids.append(room.id)
                else: # Create New
                    room = RoomType.objects.create(
                        hotel=hotel,
                        name=name,
                        room_type=r_class,
                        max_guest=guests,
                        price_per_night=price,
                        total_rooms=count,
                        amenities=amenities_list
                    )
                    processed_room_ids.append(room.id)
                
                # Room Media Logic
                # 1. Process Deletions
                deleted_photos_data = request.POST.get(f'deleted_room_photos_{idx}', '[]')
                try:
                    deleted_photos_ids = json.loads(deleted_photos_data)
                    if deleted_photos_ids:
                        RoomPhoto.objects.filter(id__in=deleted_photos_ids, room=room).delete() 
                except: pass

                # 2. Add New Media
                room_media = request.FILES.getlist(f'room_photos_{idx}')
                for f in room_media:
                    RoomPhoto.objects.create(room=room, media_file=f)

            # Cleanup: Remove rooms not present in the update
            if processed_room_ids:
                hotel.rooms.exclude(id__in=processed_room_ids).delete()

            # 5. Global Gallery Sync
            # 1. Process Gallery Deletions
            deleted_gallery_data = request.POST.get('deleted_gallery_photos', '[]')
            try:
                deleted_gallery_ids = json.loads(deleted_gallery_data)
                if deleted_gallery_ids:
                    HotelImage.objects.filter(id__in=deleted_gallery_ids, hotel=hotel).delete()
            except: pass

            # 2. Add New Gallery Media
            gallery_files = request.FILES.getlist('property_images')
            for f in gallery_files:
                HotelImage.objects.create(hotel=hotel, image_path=f)

            messages.success(request, f"Global Property Dossier for '{hotel.name}' has been securely updated.")
            return redirect('my_hotels')

        except Exception as e:
            logger.error(f"[Edit Hotel Error] {str(e)}")
            messages.error(request, f"Protocol Failure: {str(e)}")

    # Prefetch data for elite rendering
    # We use .all() to ensure we get all RoomType objects linked to this hotel
    rooms = hotel.rooms.all().prefetch_related('photos')
    gallery = hotel.images.all()
    
    return render(request, 'hotels/edit_hotel.html', {
        'hotel': hotel,
        'rooms': rooms,
        'gallery': gallery,
        'service_choices': HOTEL_SERVICE_CHOICES,
        'is_edit': True # Context flag for high-fidelity UI
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
    if hotel_id:
        hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)

    room = None
    if room_id and hotel:
        room = get_object_or_404(RoomType, id=room_id, hotel=hotel)

    if request.method == "POST":
        try:
            name = request.POST.get("name")
            room_class = request.POST.get("room_class", "STANDARD")
            max_guests = int(request.POST.get("max_guests", 2))
            base_price = float(request.POST.get("base_price", 0))
            inventory = int(request.POST.get("inventory_count", 1))

            amenities_data = request.POST.get("amenities", "[]")

            try:
                amenities_list = json.loads(amenities_data)
            except:
                amenities_list = []

            # If hotel not selected
            if not hotel:
                messages.error(request, "Please select a hotel first.")
                return redirect("hotels:manage_rooms")

            # EDIT
            if room:
                room.name = name
                room.room_class = room_class
                room.max_guests = max_guests
                room.base_price = base_price
                room.inventory_count = inventory
                room.amenities = amenities_list
                room.save()

                messages.success(request, f"Room '{name}' updated successfully.")

            # CREATE
            else:
                room = RoomType.objects.create(
                    hotel=hotel,
                    name=name,
                    room_class=room_class,
                    max_guests=max_guests,
                    base_price=base_price,
                    inventory_count=inventory,
                    amenities=amenities_list
                )

                messages.success(request, f"New Room '{name}' created successfully.")

            # Upload photos
            room_photos = request.FILES.getlist("room_photos")

            for photo in room_photos:
                RoomPhoto.objects.create(
                    room_category=room,
                    media_file=photo
                )

            return redirect("hotels:manage_rooms_hotel", hotel_id=hotel.id)
        
        except Exception as e:
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
            booking_status='confirm',
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

@hotel_admin_required
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

@hotel_admin_required
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

@hotel_admin_required
def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    offer.delete()
    messages.success(request, "Offer terminated.")
    return redirect('hotels:offers')

@hotel_admin_required
def submit_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, hotel__owner=request.user)
    offer.status = 'PENDING'
    offer.save()
    messages.success(request, "Offer submitted for approval.")
    return redirect('hotels:offers')

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