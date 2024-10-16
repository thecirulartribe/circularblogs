from django.urls import path
from .views import index, blog, offer, suggestion, aboutus, categories, get_blog, thankyou, category_wise_count, terms_and_condition, privacy_policy
urlpatterns = [
    path('', index, name='recent'),
    path('offer', offer, name='offer'),
    path('suggestions', suggestion, name='suggestion'),
    path('aboutus', aboutus, name='aboutus'),
    path('blog/<str:url>', blog),
    path('category/<str:category>', categories),
    path('get_blog/', get_blog),
    path('thankyou/', thankyou),
    path('categorycount/', category_wise_count, name="count"),
    path('terms-and-condition/', terms_and_condition, name="terms"),
    path('privacy-policy/', privacy_policy, name="privacy")
]

