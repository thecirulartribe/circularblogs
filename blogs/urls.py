from django.urls import path
from .views import (index, blog, offer, suggestion, write_for_us, aboutus, categories, get_blog, thankyou,
                    terms_and_condition, privacy_policy, cookie_policy)
urlpatterns = [
    path('', index, name='recent'),
    path('offer/', offer, name='offer'),
    path('suggestions/', suggestion, name='suggestion'),
    path('write-for-us/', write_for_us, name='write_for_us'),
    path('aboutus/', aboutus, name='aboutus'),
    path('blog/<str:url>', blog, name='view_blog'),
    path('category/<str:category>', categories),
    path('get_blog/', get_blog),
    path('thankyou', thankyou, name="thankyou"),
    path('terms-and-condition/', terms_and_condition, name="terms and conditions"),
    path('privacy-policy/', privacy_policy, name="privacy policy"),
    path('cookie-policy/', cookie_policy, name="cookie policy"),
]
