from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Hotel(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    HOTEL_TYPES = [
        ('5_STAR', '5 Star Premium'),
        ('4_STAR', '4 Star Luxury'),
        ('3_STAR', '3 Star Business'),
        ('RESORT', 'Resort / Villa'),
        ('HOTEL', 'Hotel'),
        ('BOUTIQUE', 'Boutique Hotel'),
        ('BUSINESS', 'Business Hotel'),
        ('BUDGET', 'Budget Hotel'),
        ('LUXURY', 'Luxury Hotel'),
        ('HERITAGE', 'Heritage Hotel'),
        ('AIRPORT', 'Airport Hotel'),
        ('BEACH_RESORT', 'Beach Resort'),
        ('HILL_RESORT', 'Hill Resort'),
        ('SERVICED_APT', 'Serviced Apartments'),
        ('VACATION_RENTAL', 'Vacation Rentals'),
        ('HOMESTAY', 'Homestay'),
        ('GUESTHOUSE', 'Guest House'),
        ('HOSTEL', 'Hostel'),
        ('LODGE', 'Lodge'),
        ('MOTEL', 'Motel'),
        ('VILLA', 'Villa'),
        ('ECO_RESORT', 'Eco Resort'),
        ('WELLNESS', 'Wellness Retreat'),
        ('PALACE', 'Palace Hotel'),
        ('CASINO', 'Casino Resort'),
        ('SPA_RESORT', 'Spa Resort'),
        ('GOLF_RESORT', 'Golf Resort'),
        ('SKI_RESORT', 'Ski Resort'),
        ('DESERT_CAMP', 'Desert Camp'),
        ('HOUSEBOAT', 'Houseboat'),
        ('FARM_STAY', 'Farm Stay'),
        ('OTHER', 'Other Property'),
    ]

    # --- Ownership & Identity ---
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotels')
    hotel_name = models.CharField(max_length=255)
    hotel_type = models.CharField(max_length=50, choices=HOTEL_TYPES)
    services = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    total_rooms = models.PositiveIntegerField(help_text="Total unit count of the property", default=0, blank=True)

    # --- Operational Information (Step 2C) ---
    check_in = models.TimeField(default="14:00")
    check_out = models.TimeField(default="11:00")
    cancellation_policy = models.TextField(default="Standard Rules Apply")

    # --- Compliance Documents (Files & Numbers) ---
    id_type = models.CharField(max_length=10, choices=[('AADHAAR', 'Aadhaar'), ('PAN', 'PAN Card')], default='AADHAAR')
    id_number = models.CharField(max_length=20, help_text="Aadhaar or PAN Number", null=True, blank=True)
    doc_mandatory = models.FileField(upload_to='compliance/identity/', help_text="Primary ID File", null=True, blank=True)
    
    govt_reg_number = models.CharField(max_length=50, help_text="Government Registration Number", null=True, blank=True)
    doc_certificate = models.FileField(upload_to='compliance/certificate/', help_text="Govt Certificate File", null=True, blank=True)
    
    gst_number = models.CharField(max_length=15, help_text="GST Identification Number", null=True, blank=True)
    doc_gst = models.FileField(upload_to='compliance/gst/', help_text="GST Certificate File", null=True, blank=True)

    # --- Financial Layer (Optional/Removed from UI) ---
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)
    account_holder = models.CharField(max_length=100, null=True, blank=True)

    # --- Geolocation Layer ---
    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    lng = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)

    # --- System Status ---
    status = models.CharField(
        max_length=15, 
        choices=[
            ('DRAFT', 'Draft'),
            ('PENDING', 'Pending Review'),
            ('LIVE', 'Live & Active'),
            ('REJECTED', 'Rejected / Action Required'),
        ], 
        default='PENDING'
    )
    verification_remarks = models.TextField(blank=True, null=True, help_text="Feedback from Super Admin")
    is_live = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_revenue(self):
        """Total revenue from all bookings for this hotel"""
        from bookings.models import Booking
        from django.db.models import Sum
        return Booking.objects.filter(hotel=self).aggregate(total=Sum('total_price'))['total'] or 0

    @property
    def avg_rating(self):
        """Average rating from all reviews for this hotel"""
        from reviews.models import Review
        from django.db.models import Avg
        return Review.objects.filter(hotel=self).aggregate(avg=Avg('rating'))['avg'] or 5.0

    @property
    def image(self):
        """Returns the primary image for the hotel, or the first one if no primary is set."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image_path
        first = self.images.first()
        if first:
            return first.image_path
        return None

    def __str__(self):
        return f"{self.hotel_name} ({self.city})"

class RoomType(models.Model):
    ROOM_CATEGORIES = [
        ('STANDARD', 'Standard Room'),
        ('DELUXE', 'Deluxe Room'),
        ('SUITE', 'Suite'),
        ('LUXURY', 'Luxury / Presidential Room'),
        ('ECONOMY', 'Economy Room'),
        ('PREMIUM', 'Premium Room'),
        ('EXECUTIVE', 'Executive Room'),
        ('CLUB', 'Club Room'),
        ('PRESIDENTIAL', 'Presidential Suite'),
        ('ROYAL', 'Royal Suite'),
        ('FAMILY', 'Family Room'),
        ('SPECIALTY', 'Specialty Room'),
        ('DORM', 'Dormitory Bed'),
        ('PRIVATE', 'Private Room'),
        ('CUSTOM', 'Custom Category'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_category_name = models.CharField(max_length=100, help_text="e.g. Deluxe Garden View", null=True, blank=True)
    room_type = models.CharField(max_length=20, choices=ROOM_CATEGORIES)
    price_per_night = models.PositiveIntegerField(default=0, verbose_name="Price per Night")
    max_guest = models.PositiveIntegerField(default=2, verbose_name="Max Guests")
    room_size = models.PositiveIntegerField(default=0, help_text="Room size in sqft", verbose_name="Room Size")
    total_rooms = models.PositiveIntegerField(help_text="Inventory count for this specific type")
    room_image = models.ImageField(upload_to='room_categories/', null=True, blank=True)
    amenities = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.room_type} at {self.hotel.hotel_name}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image_path = models.ImageField(upload_to='property_gallery/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Offer(models.Model):
    OFFER_TYPES = [
        ('PERCENTAGE', 'Percentage Discount'),
        ('FLAT', 'Flat Discount'),
        ('SEASONAL', 'Seasonal Offer'),
        ('EARLY_BIRD', 'Early Bird Offer'),
        ('LAST_MINUTE', 'Last Minute Deal'),
        ('WEEKEND', 'Weekend Offer'),
        ('COUPON', 'Coupon Code Offer'),
        ('MIN_STAY', 'Minimum Stay Offer'),
        ('BULK', 'Bulk Booking Discount'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SCHEDULED', 'Scheduled'),
        ('LIVE', 'Live'),
        ('EXPIRED', 'Expired'),
    ]

    APPLICABILITY_CHOICES = [
        ('ALL', 'Entire Hotel'),
        ('CATEGORY', 'Selected Room Categories'),
        ('ROOM', 'Specific Rooms'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='offers')
    name = models.CharField(max_length=100, verbose_name="Offer Title")
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES, default='PERCENTAGE')
    
    # Discount Details
    discount_type = models.CharField(max_length=20, choices=[('PERCENT', '%'), ('FIXED', '₹')], default='PERCENT')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Max ₹ discount possible")
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Applicability
    applicability = models.CharField(max_length=20, choices=APPLICABILITY_CHOICES, default='ALL')
    room_categories = models.JSONField(default=list, blank=True, help_text="IDs of room types this applies to.")
    specific_rooms = models.JSONField(default=list, blank=True, help_text="Specific room identifiers if applicable.")
    
    # Validity
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    blackout_dates = models.JSONField(default=list, blank=True, help_text="List of specific dates (ISO format) where offer is NOT valid.")
    applicable_days = models.JSONField(default=list, blank=True, help_text="List of days (0-6) where this offer is valid.")
    
    # Booking Conditions
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Min Booking Amount")
    min_nights = models.PositiveIntegerField(default=1, verbose_name="Min Nights Stay")
    max_nights = models.PositiveIntegerField(null=True, blank=True, verbose_name="Max Nights Stay")
    advance_booking_days = models.PositiveIntegerField(default=0, help_text="Days in advance to book")
    last_minute_window = models.PositiveIntegerField(default=0, help_text="Book within X days of check-in")
    
    # Usage Limits
    max_usage = models.PositiveIntegerField(default=0, help_text="0 for unlimited")
    per_user_limit = models.PositiveIntegerField(default=1)
    redemption_count = models.PositiveIntegerField(default=0)
    
    # Logic & Approval Flow
    is_stackable = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='DRAFT')
    rejection_reason = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.hotel.hotel_name})"

    def update_status(self):
        """Logic to automatically transition status based on dates and approval."""
        from django.utils import timezone
        now = timezone.now()

        if self.status in ['DRAFT', 'PENDING', 'REJECTED']:
            return self.status

        # If approved, check dates
        if self.status in ['APPROVED', 'SCHEDULED', 'LIVE', 'EXPIRED']:
            if self.valid_to < now:
                self.status = 'EXPIRED'
            elif self.valid_from > now:
                self.status = 'SCHEDULED'
            else:
                self.status = 'LIVE'

        return self.status

    @property
    def is_currently_active(self):
        """Returns True if offer is live"""
        self.update_status()
        return self.status == 'LIVE'

class ChangeRequest(models.Model):
    CATEGORY_CHOICES = [
        ('IDENTITY', 'Property Identity'),
        ('INVENTORY', 'Room Inventory'),
        ('GALLERY', 'Photo Gallery'),
        ('OPS', 'Policies & Ops'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='change_requests')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    requested_data = models.JSONField(help_text="The proposed new data")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(blank=True, null=True, help_text="Admin feedback")
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Edit Request: {self.category} for {self.hotel.hotel_name}"

class LocationHistory(models.Model):
    """Stores a history of verified geo-locations during onboarding."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location_history')
    lat = models.DecimalField(max_digits=12, decimal_places=9)
    lng = models.DecimalField(max_digits=12, decimal_places=9)
    formatted_address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    
    # Contextual Metadata
    location_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    review_count = models.PositiveIntegerField(default=0)
    image_reference = models.URLField(max_length=500, null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Location Histories"

    def __str__(self):
        return f"{self.location_name or self.city or 'Unknown Area'} - {self.user.email}"