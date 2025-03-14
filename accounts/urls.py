from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, dashboard_view, activate

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
