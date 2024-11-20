from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog

class StaticSitemap(Sitemap):
    def items(self):
        return ['recent', 'offer', 'suggestion', 'aboutus']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    def items(self):
        return Blog.objects.all().order_by('-pk')

    def lastmod(self,obj):
        return obj.updated_at