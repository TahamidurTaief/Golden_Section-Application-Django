from django.shortcuts import render, get_object_or_404
from .models import Provider


def provider_list(request):
    """Display list of all providers"""
    providers = Provider.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'providers': providers,
    }
    return render(request, 'providers.html', context)


def provider_detail(request, pk):
    """Display provider detail page"""
    provider = get_object_or_404(Provider, pk=pk, is_active=True)
    services = provider.services.filter(is_active=True)
    
    context = {
        'provider': provider,
        'services': services,
    }
    return render(request, 'provider_details.html', context)
