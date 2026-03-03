from django.urls import include, path
from . import views

app_name = "customer"
urlpatterns = [
    # Customer homepage
    path('', views.customer_search, name="home"),
    path('search_results/', views.search_results, name="search_results"),
    
    
    # Hotel and Room details
    path('hotel/<int:pk>/', views.hotel_detail, name="hotel_detail"),
    path('room/<int:room_id>/', views.room_select, name="room_select"),

    # Booking details
    path("book/<int:hotel_id>/<int:room_id>/", views.booking_details, name="booking_details"),
    path('booking_success/', views.booking_success, name="booking_success"),
    path("confirm/", views.confirm_booking, name="confirm_booking"),
    # Review add
    path('add-review/<int:hotel_id>/', views.add_review, name="add_review"),
]
