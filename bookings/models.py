from django.db import models
from accounts.models import User
from hotels.models import Hotel, RoomType


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    checkin_date = models.DateField()
    checkout_date = models.DateField()

    aadhaar_id = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, default="cash")
    booking_status = models.CharField(max_length=20, default="pending")
    
    cancel_reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.room}"
