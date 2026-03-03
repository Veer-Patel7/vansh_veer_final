from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # customer
    path('login/', views.customer_login, name="customer_login"),
    path('signup/', views.customer_signup, name="customer_signup"),
    path("auth/", views.auth_view, name="auth"),
    
    # hotel admin
    path("hotel/login/", views.hotel_login, name="hotel_login"),
    path("hotel/signup/", views.hotel_signup, name="hotel_signup"),

    # super admin login
    path('super/', views.super_login, name="super_login"),
    
    # forgot-password
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-reset-otp/", views.verify_reset_otp, name="verify_reset_otp"),
    path("set-new-password/", views.set_new_password, name="set_new_password"),
    
    # otp
    path('verify/', views.verify, name="verify"),

    # logout
    path('logout/', views.user_logout, name="logout"),
]
