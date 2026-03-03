from django.db import models
from hotels.models import Hotel

class HotelCommission(models.Model):

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()

    total_bookings = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    commission_percent = models.IntegerField(default=10)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    penalty_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    STATUS = (
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
    )

    status = models.CharField(max_length=20, choices=STATUS, default="unpaid")

    due_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def total_payable(self):
        return self.commission_amount + self.penalty_amount
