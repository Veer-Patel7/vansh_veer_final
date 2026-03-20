from django.db import models
from django.conf import settings
from hotels.models import Hotel, RoomType
from django.core.exceptions import ValidationError
from decimal import Decimal


class Booking(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="app_bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="app_hotel_bookings")
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="app_room_bookings")

    # Offer Integration
    applied_offer = models.ForeignKey('hotels.Offer', on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    checkin_date = models.DateField()
    checkout_date = models.DateField()

    total_guests = models.SmallIntegerField()
    adults = models.SmallIntegerField()
    children = models.SmallIntegerField()

    payment_method = models.CharField(max_length=20, default="cash")
    booking_status = models.CharField(max_length=20, default="confirmed")

    cancel_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.total_guests != self.adults + self.children:
            raise ValidationError("Total guests must equal adults + children")

        if self.checkin_date >= self.checkout_date:
            raise ValidationError("Checkout date must be after checkin date")

    def save(self, *args, **kwargs):

        nights = (self.checkout_date - self.checkin_date).days
        self.base_price = nights * self.room.price_per_night

        # Apply offer discount
        if self.applied_offer:
            discount_percent = self.applied_offer.discount_percent
            self.discount_amount = (self.base_price * discount_percent) / 100
        else:
            self.discount_amount = 0

        self.total_price = self.base_price - self.discount_amount

        super().save(*args, **kwargs)

    @property
    def commission(self):
        return round(self.total_price * Decimal("0.10"), 2)

    def __str__(self):
        return f"{self.user.email} - {self.room}"
    