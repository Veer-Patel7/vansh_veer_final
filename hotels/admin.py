from django.contrib import admin
from .models import Hotel, RoomType, HotelImage, RoomImage


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3   # number of empty image fields


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline]