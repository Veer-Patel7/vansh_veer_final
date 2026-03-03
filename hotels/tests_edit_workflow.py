from django.test import TestCase, Client
from django.urls import reverse
from user_access.models import User
from .models import Hotel, ChangeRequest, RoomType
import json

class PropertyEditWorkflowTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username='hotelowner', password='password123', role='OWNER')
        self.admin = User.objects.create(username='superadmin', password='password123', role='ADMIN')
        self.client = Client()
        
        # Manual Session Login
        session = self.client.session
        session['user_id'] = self.owner.id
        session.save()
        
        self.hotel = Hotel.objects.create(
            owner=self.owner,
            hotel_name="Original Hotel",
            hotel_type="HOTEL",
            address="123 Original St",
            city="Origin City",
            status="LIVE",
            is_live=True
        )
        
        self.room = RoomType.objects.create(
            hotel=self.hotel,
            room_type="STANDARD",
            price_per_night=1000,
            max_guests=2,
            total_rooms=5
        )

    def test_owner_submit_identity_edit_request(self):
        # Double check session
        s = self.client.session
        with open('debug_test.txt', 'a') as f:
            f.write(f"Session user_id: {s.get('user_id')}\n")
            f.write(f"Owner id: {self.owner.id}\n")

        payload = {
            'hotel_name': 'Updated Hotel Name',
            'description': 'New description',
            'hotel_type': '5_STAR',
            'address': '456 New Blvd',
            'city': 'New City',
            'state': 'New State',
            'pincode': '999999'
        }
        
        url = reverse('hotels:submit_edit_request', kwargs={'hotel_id': self.hotel.id, 'category': 'IDENTITY'})
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        
        with open('debug_test.txt', 'a') as f:
            f.write(f"Response status: {response.status_code}\n")
            if response.status_code != 200:
                f.write(f"Response content: {response.content.decode()[:500]}\n")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ChangeRequest.objects.filter(hotel=self.hotel, category='IDENTITY', status='PENDING').exists())
