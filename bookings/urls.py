from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('success/<str:booking_reference>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
