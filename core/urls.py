from django.urls import path,include
from . import views
urlpatterns=[
    path('',views.landing,name='landing'),
    path('features/', views.features, name='features'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('chat/', views.chat_page, name='chat_page'),
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),
    path('checkout/<int:room_type_id>/', views.checkout_view, name='checkout'),
    path('api/apply-coupon/', views.apply_coupon_api, name='apply_coupon'),
]