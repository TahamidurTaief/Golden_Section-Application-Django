from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('services/', include('services.urls')),
    path('providers/', include('providers.urls')),
    path('quotations/', include('quotations.urls')),
    path('bookings/', include('bookings.urls')),
    path('pages/', include('content.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)