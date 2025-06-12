from django.contrib.sitemaps import Sitemap
from .models import Agent

class AgentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Agent.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

    def location(self, obj):
        return obj.get_absolute_url() 
 
 