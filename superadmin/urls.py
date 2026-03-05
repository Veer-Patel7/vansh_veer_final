from django.urls import path
from . import views

app_name = "superadmin"

urlpatterns = [
    path('dashboard/', views.dashboard, name="super_dashboard"),
    path("profile/", views.profile, name="profile"),
    
    # OWNER LOGIN APPROVAL
    path('owners/', views.owners, name="owners"),
    path('approve-owner/<int:user_id>/', views.approve_owner),
    path('disable-owner/<int:user_id>/', views.disable_owner),
    path('enable-owner/<int:user_id>/', views.enable_owner),
    
    # HOTEL REGISTER APPROVAL
    path('hotels/', views.hotels_approve),
    path('hotel/<int:hotel_id>/', views.hotel_detail_view, name='hotel_detail'),
    path('approve-hotel/<int:hotel_id>/', views.approve_hotel),
    path('block-hotel/<int:hotel_id>/', views.block_hotel),
    path('reject-hotel/<int:hotel_id>/', views.reject_hotel),

    # BOOKING MANAGE
    path("bookings/", views.bookings_manage),
    path("update-booking/<int:booking_id>/", views.update_booking),

    # PAYMENTS MAIN PAGE
    path('payments/', views.payments_dashboard),
    # COMMISSION
    path('payments/generate/', views.generate_commission),
    path('payments/invoices/', views.commissions),
    path('payments/mark-paid/<int:id>/', views.mark_paid),
    
    # CUSTOMER MANAGE
    path("customers/", views.customers_manage),
    path("blacklist/<int:user_id>/", views.blacklist_customer),
    path("unblock/<int:user_id>/", views.unblock_customer),

    # REVIEW  MODERATE
    path("reviews/", views.reviews_moderate),
    path("approve-review/<int:id>/", views.approve_delete_review),
    path("reject-review/<int:id>/", views.reject_delete_review),
    path("fake-review/<int:id>/", views.mark_fake_review),
    
    
]