"""
Context processors for global template variables
"""
from site_config.models import SiteConfiguration


def site_settings(request):
    """
    Add site configuration to all templates
    Usage in templates: {{ site_config.site_name }}
    """
    return {
        'site_config': SiteConfiguration.load()
    }
