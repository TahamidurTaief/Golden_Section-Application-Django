"""
Context processors for global template variables
"""
from site_config.models import SiteConfiguration
from categories.models import Category

def site_settings(request):
    """
    Add site configuration to all templates
    Usage in templates: {{ site_config.site_name }}
    """
    return {
        'site_config': SiteConfiguration.load()
    }


def navbar(request):
    categories = Category.objects.all()
    return {
        'nav_categories': categories  # এই নামেই টেমপ্লেটে লুপ চালাতে হবে
    }