from django.db import models
from django.conf import settings
from hotels.models import Hotel, RoomType
from django.core.exceptions import ValidationError


class Booking(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="app_bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="app_hotel_bookings")
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name="app_room_bookings")

    checkin_date = models.DateField()
    checkout_date = models.DateField()

    total_guests = models.SmallIntegerField()
    adults = models.SmallIntegerField()
    children = models.SmallIntegerField()

    payment_method = models.CharField(max_length=20, default="cash")
    booking_status = models.CharField(max_length=20, default="confirm")
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    cancel_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.total_guests != self.adults + self.children:
            raise ValidationError("Total guests must equal adults + children")

        if self.checkin_date >= self.checkout_date:
            raise ValidationError("Checkout date must be after checkin date")

    def __str__(self):
        return f"{self.user.email} - {self.room}"