"""
URL configuration for circular_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from django.contrib.sitemaps.views import sitemap
from blogs.sitemaps import *

sitemaps = {
    'static' : StaticSitemap,
    'blogs': BlogSitemap,
}
urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('ads.txt/', TemplateView.as_view(template_name="ads.txt", content_type="text/plain")),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('adimanav/', admin.site.urls),
    path('', include('blogs.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "blogs.views.page_not_found_view"
handler500 = "blogs.views.server_error"
