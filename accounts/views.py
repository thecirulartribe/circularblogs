from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
from blogs.models import Blog
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.html import strip_tags

User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Disable account until email is verified
            user.save()

            # Send verification email
            send_verification_email(user, request)

            return render(request, "accounts/email_sent.html")  # Show success page
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        blogger_group, created = Group.objects.get_or_create(name='blogger')
        user.groups.add(blogger_group)
        user.save()
        login(request, user)
        return redirect('dashboard')  # Redirect to dashboard after activation
    else:
        return render(request, "accounts/invalid_verification.html")  # Show "Invalid Link" page


def send_verification_email(user, request):
    """Send a verification email with an HTML template."""
    current_site = get_current_site(request)
    mail_subject = "Activate Your Account"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"

    # Render HTML template
    html_message = render_to_string("accounts/email_verification.html", {
        "user": user,
        "activation_link": activation_link,
    })

    # Strip HTML tags for a plain text version
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=plain_message,  # Plain text message for email clients that don't support HTML
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")  # Attach HTML version
    email.send()


@login_required
def dashboard_view(request):
    # List blogs authored by the current user
    blogs = Blog.objects.filter(author_user=request.user)
    return render(request, 'accounts/dashboard.html', {'blogs': blogs})