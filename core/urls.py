from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('home-content/', views.home_content, name='home_content'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('categories/', views.categories, name='categories'),
    path('search-categories/', views.search_categories, name='search_categories'),
    path('search-subcategories/', views.search_subcategories, name='search_subcategories'),
    path('service/<int:pk>/', views.service_details, name='service_details'),
    path('booking/', views.booking, name='booking'),
    path('service/request/', views.service_request, name='service_request'),
    path('service/request/step/', views.service_request_step, name='service_request_step'),
    path('service/request/data/', views.get_service_request_data, name='service_request_data'),
]