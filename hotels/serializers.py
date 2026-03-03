from rest_framework import serializers
from .models import Hotel, RoomType, HotelImage

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ['id', 'image_path', 'is_primary', 'uploaded_at']

class RoomTypeSerializer(serializers.ModelSerializer):
    # Provides the human-readable name for the choice field
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)

    class Meta:
        model = RoomType
        fields = [
            'id', 'room_type', 'room_type_display', 'price_per_night', 
            'max_guests', 'total_rooms'
        ]

# HotelPolicySerializer removed as fields are merged into Hotel

class HotelSerializer(serializers.ModelSerializer):
    # Nested Serializers to show related data
    rooms = RoomTypeSerializer(many=True, read_only=True)
    images = HotelImageSerializer(many=True, read_only=True)
    
    # Custom field to calculate maturity progress
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            'id', 'hotel_name', 'hotel_type', 'description', 'total_rooms',
            'city', 'state', 'address', 'lat', 'lng', 'status', 'is_live',
            'rooms', 'images', 'completion_percentage',
            'check_in', 'check_out', 'cancellation_policy'
        ]

    def get_completion_percentage(self, obj):
        """Logic to calculate how much of the property profile is finished"""
        score = 0
        if obj.rooms.exists(): score += 50
        if obj.images.count() >= 5: score += 50
        return score