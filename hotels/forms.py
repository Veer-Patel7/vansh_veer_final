from django import forms
from .models import Hotel, RoomType, HotelImage, Offer

class HotelDeploymentForm(forms.ModelForm):
    """
    Handles the primary registration of the property.
    Divided into 4 logical modules in the frontend.
    """
    class Meta:
        model = Hotel
        fields = [
            'hotel_name', 'hotel_type', 'total_rooms', 'description',
            'check_in', 'check_out', 'cancellation_policy',
            'id_type', 'id_number', 'doc_mandatory',
            'govt_reg_number', 'doc_certificate',
            'gst_number', 'doc_gst',
            'city', 'state', 'pincode', 'address', 'lat', 'lng'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Overview of the property...', 'required': 'true'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'required': 'true'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'required': 'true'}),
            'cancellation_policy': forms.Textarea(attrs={'rows': 3, 'required': 'true'}),
            'address': forms.TextInput(attrs={'placeholder': 'Search for address or drag map...', 'id': 'location-search', 'class': 'input-address', 'required': 'true'}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            'total_rooms': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'pincode': forms.HiddenInput(),
        }
    
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not pincode:
            return pincode
        # Relaxing for map-based auto-population
        return pincode

class RoomTypeForm(forms.ModelForm):
    """
    Handles the creation and editing of room inventory tiers.
    """
    class Meta:
        model = RoomType
        fields = ['name', 'room_type', 'price_per_night', 'max_guest', 'total_rooms']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'console-input'}),
        }

class HotelImageForm(forms.ModelForm):
    """
    Used for single image uploads or as a base for multi-upload.
    """
    class Meta:
        model = HotelImage
        fields = ['image_path', 'is_primary']

class HotelPolicyForm(forms.ModelForm):
    """
    Handles hotel policies like check-in/out and cancellation.
    These fields are part of the Hotel model.
    """
    class Meta:
        model = Hotel
        fields = ['check_in', 'check_out', 'cancellation_policy']
        widgets = {
            'check_in': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'e.g. 14:00'}),
            'check_out': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'e.g. 11:00'}),
            'cancellation_policy': forms.Textarea(attrs={'class': 'console-input', 'rows': 3}),
        }

class OfferForm(forms.ModelForm):
    """
    Handles creation and editing of promotional offers.
    """
    class Meta:
        model = Offer
        fields = [
            'name', 'offer_type', 'discount_type', 'discount_value', 
            'max_discount_limit', 'coupon_code', 'applicability',
            'room_categories', 'specific_rooms', 'min_amount', 'min_nights',
            'max_nights', 'advance_booking_days', 'last_minute_window',
            'valid_from', 'valid_to', 'blackout_dates', 'applicable_days', 
            'max_usage', 'per_user_limit', 'is_stackable', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'Offer Title'}),
            'offer_type': forms.Select(attrs={'class': 'console-input'}),
            'discount_type': forms.Select(attrs={'class': 'console-input'}),
            'discount_value': forms.NumberInput(attrs={'class': 'console-input'}),
            'max_discount_limit': forms.NumberInput(attrs={'class': 'console-input'}),
            'coupon_code': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'Optional'}),
            'applicability': forms.Select(attrs={'class': 'console-input'}),
            'valid_from': forms.DateTimeInput(attrs={'class': 'console-input', 'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'class': 'console-input', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'console-input'}),
        }

class HotelIdentityForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = [
            "hotel_name", "hotel_type", "total_rooms", "description",
            "address", "city", "state", "pincode",
            "gst_number", "id_type", "id_number",
        ]
        widgets = {
            'hotel_name': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'e.g. Grand Plaza'}),
            'hotel_type': forms.Select(attrs={'class': 'console-input'}),
            'total_rooms': forms.NumberInput(attrs={'class': 'console-input', 'placeholder': '0'}),
            'description': forms.Textarea(attrs={'class': 'console-input', 'rows': 4, 'placeholder': 'Write a compelling property summary...'}),
            'address': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'Street address...'}),
            'city': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'City name'}),
            'state': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'State/Province'}),
            'pincode': forms.TextInput(attrs={'class': 'console-input', 'placeholder': '######'}),
            'gst_number': forms.TextInput(attrs={'class': 'console-input uppercase', 'placeholder': 'GSTIN'}),
            'id_type': forms.Select(attrs={'class': 'console-input'}),
            'id_number': forms.TextInput(attrs={'class': 'console-input', 'placeholder': 'Card Number'}),
        }