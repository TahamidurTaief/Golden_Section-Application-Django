from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('create/', views.create_service_request, name='create_request'),
    path('request/', views.service_request_view, name='request'),
    path('request/<int:service_id>/', views.service_request_view, name='request_with_service'),
]
