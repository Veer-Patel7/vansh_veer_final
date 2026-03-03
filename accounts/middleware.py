from django.utils.deprecation import MiddlewareMixin
from .models import User
from django.contrib.auth.models import AnonymousUser

class ManualAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
