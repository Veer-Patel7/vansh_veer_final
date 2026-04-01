from django.contrib import admin
from .models import Hotel, RoomType, HotelImage


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3   # number of empty image fields


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]


admin.site.register(RoomType)