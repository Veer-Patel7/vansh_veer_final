from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from user_access.models import User
from .models import Hotel, RoomType, HotelImage

class HotelOnboardingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testowner', password='password123', role='OWNER')
        self.client = Client()
        # Manual Session Login
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

    def test_add_hotel_with_images(self):
        # Create dummy images
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        room_img = SimpleUploadedFile('room.gif', small_gif, content_type='image/gif')
        gallery_img1 = SimpleUploadedFile('gallery1.gif', small_gif, content_type='image/gif')
        gallery_img2 = SimpleUploadedFile('gallery2.gif', small_gif, content_type='image/gif')
        doc_img = SimpleUploadedFile('doc.gif', small_gif, content_type='image/gif')

        data = {
            'hotel_name': 'Test luxury Hotel',
            'hotel_type': 'HOTEL',
            'total_rooms': 10,
            'description': 'A nice place',
            'city': 'Test City',
            'state': 'Test State',
            'pincode': '123456',
            'address': '123 Test Lane',
            'lat': 12.345678,
            'lng': 78.901234,
            'bank_name': 'Test Bank',
            'account_holder': 'Test Owner',
            'account_number': '1234567890',
            'ifsc_code': 'IFSC001',
            'check_in': '14:00',
            'check_out': '11:00',
            'cancellation_policy': 'No cancellation',
            'room_name_1': 'Deluxe Room',
            'room_class_1': 'DELUXE',
            'room_price_1': 5000,
            'room_guests_1': 2,
            'room_count_1': 5,
            'services': ['wifi', 'parking'],
            'id_number': '1234567890',
            'govt_reg_number': 'GOV123',
            'doc_mandatory': doc_img,
        }
        
        # Files data
        files = {
            'room_image_1': room_img,
            'property_images': [gallery_img1, gallery_img2],
        }

        # Merge files into data
        data.update(files)

        response = self.client.post(reverse('hotels:hotelregister'), data=data, follow=True)
        
        # If it fails, print errors for debugging
        if response.status_code != 200 or not Hotel.objects.filter(hotel_name='Test luxury Hotel').exists():
            if 'form' in response.context:
                print(f"DEBUG_FORM_ERRORS: {response.context['form'].errors}")
            else:
                print(f"DEBUG_RESPONSE_CODE: {response.status_code}")
                print(f"DEBUG_RESPONSE_CONTENT: {response.content.decode()[:500]}")
            self.fail("Onboarding failed, check DEBUG output")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Hotel.objects.filter(hotel_name='Test luxury Hotel').exists())
        hotel = Hotel.objects.get(hotel_name='Test luxury Hotel')
        
        # Check RoomType
        self.assertEqual(hotel.rooms.count(), 1)
        room = hotel.rooms.first()
        self.assertEqual(room.room_type, 'DELUXE')
        print(f"Room Image Name: {room.room_image.name}")
        self.assertTrue(room.room_image.name != "")
        
        # Check HotelImages
        self.assertEqual(hotel.images.count(), 2)
        self.assertTrue(hotel.images.filter(is_primary=True).exists())
