from django.urls import path
from . import views

urlpatterns = [

    # hotel admin delete request
    path("request-delete/<int:id>/", views.request_delete),

    # super admin
    path("approve/<int:id>/", views.approve_delete),
    path("reject/<int:id>/", views.reject_delete),

]