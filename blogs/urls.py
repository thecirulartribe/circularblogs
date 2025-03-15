from django.urls import path
from .views import (index, blog, offer, suggestion, aboutus, categories, get_blog, thankyou,
                    terms_and_condition, privacy_policy, cookie_policy, create_blog_view, edit_blog_view, delete_blog_view)
urlpatterns = [
    path('', index, name='recent'),
    path('offer/', offer, name='offer'),
    path('suggestions/', suggestion, name='suggestion'),
    path('aboutus/', aboutus, name='aboutus'),
    path('blog/<str:url>', blog, name='view_blog'),
    path('category/<str:category>', categories),
    path('get_blog/', get_blog),
    path('thankyou', thankyou, name="thankyou"),
    path('terms-and-condition/', terms_and_condition, name="terms and conditions"),
    path('privacy-policy/', privacy_policy, name="privacy policy"),
    path('cookie-policy/', cookie_policy, name="cookie policy"),
    path('create/', create_blog_view, name='create_blog'),
    path('edit/<int:blog_id>/', edit_blog_view, name='edit_blog'),
    path('delete/<int:blog_id>/', delete_blog_view, name='delete_blog'),
]

