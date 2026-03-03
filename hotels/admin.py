from django.contrib import admin
from .models import Hotel, RoomType, HotelImage

admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(HotelImage)