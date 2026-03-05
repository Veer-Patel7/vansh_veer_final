from .models import Notification
from hotels.models import Hotel
from bookings.models import Booking
from accounts.models import User


def notifications(request):

    if request.user.is_authenticated:

        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )

        all_notifications = Notification.objects.filter(
            user=request.user
        )[:10]

        owners_count = User.objects.filter(role="hotel_admin").count()
        hotels_count = Hotel.objects.count()
        bookings_count = Booking.objects.count()

        return {
            'unread_notifications_count': unread_notifications.count(),
            'recent_notifications': all_notifications,

            # ADMIN DROPDOWN STATS
            'owners_count': owners_count,
            'hotels_count': hotels_count,
            'bookings_count': bookings_count,
        }

    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
        'owners_count': 0,
        'hotels_count': 0,
        'bookings_count': 0,
    }