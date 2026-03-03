from django.urls import path, include

from . import views


app_name = 'hotels'
# URL Patterns
urlpatterns = [
   
    # Template-based views
    path('register/', views.add_hotel, name='hotelregister'),
    path('dashboard/<int:hotel_id>/', views.hotel_dashboard, name='hotel_dashboard'),
    path('rooms/add/<int:hotel_id>/', views.create_room_type, name='create_room_type'),
    path('policy/setup/<int:hotel_id>/', views.setup_policy, name='setup_policy'),
    path('gallery/upload/<int:hotel_id>/', views.upload_images, name='upload_images'),
    path('owner/dashboard/', views.admin_dashboard_pro, name='admin_dashboard_pro'),
    path('owner/my-hotels/', views.my_hotels, name='my_hotels'),
    # Offers Workflow
    path('owner/offers/', views.offers_view, name='offers'),
    path('offers/create/', views.create_offer, name='create_offer'),
    path('offers/edit/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('offers/delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('offers/submit/<int:offer_id>/', views.submit_offer, name='submit_offer'),

    # Super Admin Verification & Offer Panel
    path('admin/verify/', views.admin_verify_list, name='admin_verify_list'),
    path('admin/verify/approve/<int:hotel_id>/', views.admin_approve_hotel, name='admin_approve_hotel'),
    path('admin/offers/', views.admin_offer_list, name='admin_offer_list'),
    path('admin/offers/review/<int:offer_id>/', views.admin_review_offer, name='admin_review_offer'),

    # Sidebar Views
    path('owner/bookings/', views.bookings_view, name='bookings'),
    path('owner/insights/', views.insights_view, name='insights'),
    
    # REVIEW
    path("reviews/", views.hotel_reviews, name="hotel_reviews"),
    path("request-delete/<int:id>/", views.request_delete_review, name="request_delete_review"),
    
    path('owner/settings/', views.settings_view, name='settings'),
    
    # Property Edit Workflow
    path('edit-detail/<int:hotel_id>/<str:category>/', views.property_edit_detail, name='property_edit_detail'),
    path('edit-submit/<int:hotel_id>/<str:category>/', views.submit_edit_request, name='submit_edit_request'),

]