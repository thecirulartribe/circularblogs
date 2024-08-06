from django.urls import path
from .views import index, blog, offer, suggestion, aboutus
urlpatterns = [
    path('', index, name='recent'),
    path('offer', offer, name='offer'),
    path('suggestions', suggestion, name='suggestion'),
    path('aboutus', aboutus, name='aboutus'),
    path('blog/<str:title>', blog),
]