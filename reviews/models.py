from django.db import models
from accounts.models import User
from hotels.models import Hotel

class Review(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField()

    recommend = models.BooleanField(default=True)

    STATUS_CHOICES = (
        ("active", "Active"),
        ("delete_request", "Delete Request"),
        ("deleted", "Deleted"),
        ("fake", "Fake"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.hotel_name} - {self.user.email}"
    
    