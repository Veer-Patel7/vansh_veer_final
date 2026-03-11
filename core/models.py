from django.db import models

from django.conf import settings

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="core_reviews" )
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='hotel_reviews', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating} stars"



class Roomtype(models.TextChoices):
    DELUXE = 'Deluxe', 'Deluxe Room'
    SUITE = 'Suite', 'Executive Suite'
    STANDARD = 'Standard', 'Standard Room'

class Room(models.Model):
    # hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms') # Removed
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=Roomtype.choices, default=Roomtype.STANDARD)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    capacity = models.IntegerField(default=2)
    
    def __str__(self):
        return f"{self.room_number} - {self.room_type} (${self.price_per_night})"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="core_bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='hotel_bookings', null=True, blank=True)
    
    # Offer Integration
    applied_offer = models.ForeignKey('hotels.Offer',on_delete=models.SET_NULL,null=True, blank=True,related_name="core_bookings_with_offer")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking for {self.user} - {self.room}"
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('SUCCESS', 'Success'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('DANGER', 'Danger'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='INFO')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"

    class Meta:
        ordering = ['-created_at']

