from django.contrib.sitemaps import Sitemap
from django.shortcuts import redirect
from store.models import Items

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['store:about-us', 'store:contact-us', 'store:terms']

    def location(self, item):
        return redirect(item)


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return Items.objects.all()
    
    def lastmod(self, obj):
        return obj.date_added
    
