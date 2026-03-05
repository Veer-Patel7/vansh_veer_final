from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import hotel_admin_required, super_admin_required
from .models import Hotel, RoomType, HotelImage, Offer, ChangeRequest, LocationHistory
import json
from django.utils import timezone
from datetime import timedelta
from .forms import HotelDeploymentForm, RoomTypeForm, HotelPolicyForm, HotelImageForm, OfferForm
from core.models import Review, Booking
from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (
    HotelSerializer, RoomTypeSerializer, 
    HotelImageSerializer
) 

from django.db import transaction

# --- 1. Property Identity (Unified Onboarding) ---
@hotel_admin_required
def add_hotel(request):
    """Professional Multi-step Hotel Onboarding View"""
    if request.method == 'POST':
        # Professional Pre-processing: Clean coordinates to avoid validation crashes
        post_data = request.POST.copy()
        for field in ['lat', 'lng']:
            val = post_data.get(field)
            if val:
                try:
                    # Round to 10 decimal places to safely fit in DecimalField
                    post_data[field] = str(round(float(val), 10))
                except (ValueError, TypeError):
                    pass
        
        form = HotelDeploymentForm(post_data, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Primary Save (Hotel Base + Policies)
                    hotel = form.save(commit=False)
                    hotel.owner = request.user
                    
                    # 2. Add Services (Step 2B)
                    services = request.POST.getlist('services')
                    hotel.services = services
                    
                    # Initial save to get ID for related objects
                    hotel.save()

                    # 3. Save Dynamic Room Types (Step 2A)
                    total_inventory = 0
                    room_idx = 1
                    while f'room_name_{room_idx}' in request.POST:
                        room_name = request.POST.get(f'room_name_{room_idx}')
                        room_class = request.POST.get(f'room_class_{room_idx}', 'STANDARD')
                        
                        # Robust Data Extraction
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
                            room_category_name=room_name,
                            room_type=room_class.upper(),
                            price_per_night=price,
                            max_guest=guests,
                            total_rooms=inventory,
                            amenities=amenities
                        )
                        
                        # Room Photo (Step 2A Individual)
                        room_photos = request.FILES.getlist(f'room_photos_{room_idx}')
                        if room_photos:
                            room.room_image = room_photos[0]
                            room.save()
                            
                        total_inventory += inventory
                        room_idx += 1

                    # 4. Save Property Gallery Images (Step 2C)
                    property_images = request.FILES.getlist('property_images')
                    for img in property_images:
                        HotelImage.objects.create(hotel=hotel, image_path=img)

                    # 5. Finalize Deployment Metadata
                    hotel.total_rooms = total_inventory
                    hotel.submitted_at = timezone.now()
                    hotel.status = 'PENDING'
                    hotel.save()

                    messages.success(request, f"Welcome to Pal! {hotel.hotel_name} is now in the verification queue.")
                    return redirect('hotels:admin_dashboard_pro')
            except Exception as e:
                import traceback
                print(f"[Onboarding Error] {traceback.format_exc()}")
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            # Enhanced Error Reporting (Professional UX)
            errors = form.errors.as_data()
            print(f"[Form Errors] {errors}")
            messages.error(request, "Please check the highlighted fields and retry.")
    else:
        form = HotelDeploymentForm()
    return render(request, 'hotels/add_hotel.html', {'form': form})

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
def hotel_dashboard(request, hotel_id):
    """Sare models ka data yahan calculate hota hai progress ke liye"""
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    
    # Logic for Completion Logic (Serializers wala formula yahan bhi kaam ayega)
    rooms = hotel.rooms.all()
    image_count = hotel.images.count()
    # Check if policy fields are filled (not default or empty)
    has_policy = bool(hotel.check_in and hotel.check_out and hotel.cancellation_policy)
    
    context = {
        'hotel': hotel,
        'rooms': rooms,
        'image_count': image_count,
        'has_rooms': rooms.exists(),
        'has_policy': has_policy,
        # Progress Calculation
        'progress': (40 if rooms.exists() else 0) + (40 if image_count >= 5 else 0) + (20 if has_policy else 0)
    }
    return render(request, 'hotels/dashboard.html', context)




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

@hotel_admin_required
def my_hotels(request):
    """List of all hotels owned by the current user"""
    owned_hotels = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotels/my_hotels.html', {'owned_hotels': owned_hotels})

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
    owned_hotels = Hotel.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(hotel__in=owned_hotels).order_by('-created_at')
    return render(request, 'hotels/bookings.html', {'bookings': bookings})

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
    # Simple JSON data response for the modal
    data = {
        'hotel_name': hotel.hotel_name,
        'hotel_type': hotel.hotel_type,
        'description': hotel.description,
        'city': hotel.city,
        'address': hotel.address,
    }
    return JsonResponse(data)

@hotel_admin_required
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