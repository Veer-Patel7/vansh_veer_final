from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        all_notifications = Notification.objects.filter(user=request.user)[:10]
        return {
            'unread_notifications_count': unread_notifications.count(),
            'recent_notifications': all_notifications
        }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }
