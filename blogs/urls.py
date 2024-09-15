from django.urls import path
from .views import index, blog, offer, suggestion, aboutus, categories, get_blog, thankyou, blog_list
urlpatterns = [
    path('', index, name='recent'),
    path('offer', offer, name='offer'),
    path('suggestions', suggestion, name='suggestion'),
    path('aboutus', aboutus, name='aboutus'),
    path('blog/<str:title>', blog),
    path('category/<str:category>', categories),
    path('get_blog/', get_blog),
    path('thankyou/', thankyou),
    path('api/blogs/', blog_list, name='blog-list'),
]

