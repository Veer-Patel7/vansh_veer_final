from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# REST API Router
router = DefaultRouter()
router.register(r'api/hotels', views.HotelViewSet, basename='hotel-api')
router.register(r'api/rooms', views.RoomTypeViewSet, basename='room-api')
router.register(r'api/gallery', views.GalleryViewSet, basename='gallery-api')

app_name = 'hotels'
# URL Patterns
urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    path('',include("core.urls")),

    # Template-based views
    path('register/', views.add_hotel, name='hotelregister'),
    path('dashboard/<int:hotel_id>/', views.hotel_dashboard, name='hotel_dashboard'),
    path('dashboard/<int:hotel_id>/', views.hotel_dashboard, name='dashboard_specific'),
    path('rooms/add/<int:hotel_id>/', views.create_room_type, name='create_room_type'),
    path('policy/setup/<int:hotel_id>/', views.setup_policy, name='setup_policy'),
    path('gallery/upload/<int:hotel_id>/', views.upload_images, name='upload_images'),
    path('owner/dashboard/', views.admin_dashboard_pro, name='admin_dashboard_pro'),
    path('owner/my-hotels/', views.my_hotels, name='my_hotels'),
    path('hotels/delete/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
    path('hotels/edit/<int:hotel_id>/', views.edit_hotel, name='edit_hotel'),
    
    #rooms
    path('rooms/add/', views.add_room, name='new_add_room'),
    path('rooms/<int:hotel_id>/add/', views.add_room, name='add_room'),
    path('rooms/<int:hotel_id>/<int:room_id>/edit/', views.add_room, name='edit_room'),
    path('rooms/', views.manage_rooms, name='manage_rooms'),
    path('rooms/<int:hotel_id>/', views.manage_rooms, name='manage_rooms_hotel'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    
    
    # Offers Workflow
    path('owner/offers/', views.offers_view, name='offers'),
    path('offers/add/', views.add_offer, name='add_offer'),
    path('offers/edit/<int:offer_id>/', views.add_offer, name='edit_offer'),
    path('offers/toggle/<int:offer_id>/', views.toggle_offer_status, name='toggle_offer_status'),
    path('offers/delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('api/offers/<int:offer_id>/usage/', views.offer_usage_details, name='offer_usage_details'),
    path('api/offers/<int:offer_id>/rooms/', views.offer_rooms_details, name='offer_rooms_details'),
    path('offers/submit/<int:offer_id>/', views.submit_offer, name='submit_offer'),

    # Super Admin Verification & Offer Panel
    path('admin/verify/', views.admin_verify_list, name='admin_verify_list'),
    path('admin/verify/approve/<int:hotel_id>/', views.admin_approve_hotel, name='admin_approve_hotel'),
    path('admin/offers/', views.admin_offer_list, name='admin_offer_list'),
    path('admin/offers/review/<int:offer_id>/', views.admin_review_offer, name='admin_review_offer'),

    # Property Edit Workflow
    path('edit-detail/<int:hotel_id>/<str:category>/', views.property_edit_detail, name='property_edit_detail'),
    path('edit-submit/<int:hotel_id>/<str:category>/', views.submit_edit_request, name='submit_edit_request'),
    

    # Sidebar Views
    path('owner/bookings/', views.bookings_view, name='bookings'),
    path('owner/insights/', views.insights_view, name='insights'),
    path('owner/reviews/', views.reviews_view, name='reviews'),
    path('owner/settings/', views.settings_view, name='settings'),
    path('api/bookings/latest/', views.api_latest_booking, name='api_latest_booking'),
    
    # Location History APIs
    path('api/location-history/', views.get_location_history, name='get_location_history'),
    path('api/location-history/add/', views.add_location_history, name='add_location_history'),
    path('api/location-history/bulk/', views.bulk_action_location_history, name='bulk_action_location_history'),
    
    
]