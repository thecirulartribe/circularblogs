from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, dashboard_view, activate, forgot_password, reset_password, email_sent, resend_verification_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
    path("signup/email-sent/<user_id>/", email_sent, name="email_sent"),
    path("signup/resend-verification/<int:user_id>/", resend_verification_email, name="resend_verification"),
]
