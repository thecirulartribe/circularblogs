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
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib import messages

User = get_user_model()

def signup(request):
  form = CustomUserCreationForm(request.POST)
  if form.is_valid():
    user = form.save(commit=False)
    user.is_active = False  # Disable account until email is verified
    user.resend_attempts = 0  # Initialize resend attempts
    user.last_resend_time = None  # Reset last resend time
    user.save()

    # Send verification email
    send_verification_email(user, request)

    return redirect(f"/accounts/signup/email-sent/{user}/")  # Show success page
  else:
    form = CustomUserCreationForm()

  return render(request, "accounts/signup.html", {"form": form})


def email_sent(request,user_id):
  attempts_remaining = 3
  try:
    user = CustomUser.objects.get(username=user_id)
    remaining_time = 0
    attempts_remaining = attempts_remaining - user.resend_attempts

    if user.last_resend_time:
      elapsed_time = (now() - user.last_resend_time).total_seconds()
      remaining_time = max(60 - int(elapsed_time), 0)  # Calculate remaining seconds

    return render(request, "accounts/email_sent.html", {"user": user, "remaining_time": remaining_time, 'attempts': attempts_remaining})

  except CustomUser.DoesNotExist:
    return redirect('/accounts/signup/')


def activate(request, uidb64, token):
  try:
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
      return redirect('/accounts/dashboard/')  # Redirect to dashboard after activation
  except:
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

def resend_verification_email(request, user_id):
  try:
    user = CustomUser.objects.get(id=user_id)

    if user.is_active:
      messages.success(request, "Your email is already verified.")
      return redirect("/accounts/login/")

    # Check if the user has exceeded 3 attempts
    if user.resend_attempts >= 3:
      user.delete()  # Delete account
      messages.error(request, "Too many resend attempts. Your account has been deleted. Please Signup again")
      return redirect("/accounts/signup/")

    # Check if at least 1 minute has passed since last resend
    if user.last_resend_time and (now() - user.last_resend_time).total_seconds() < 60:
      messages.error(request, "You can resend the verification email after 1 minute.")
      return redirect(f"/accounts/signup/email-sent/{user}/")

    # Send verification email
    send_verification_email(user, request)

    # Update resend attempts and timestamp
    user.resend_attempts += 1
    user.last_resend_time = now()
    user.save()

    messages.success(request, "Verification email resent successfully.")
    return redirect(f"/accounts/signup/email-sent/{user}/")

  except CustomUser.DoesNotExist:
    messages.error(request, "User does not exist.")
    return redirect("/accounts/signup/")


@login_required
def dashboard_view(request):
  # List blogs authored by the current user
  blogs = Blog.objects.filter(author_user=request.user)
  # Categorize blogs
  context = {
    "total_blogs": blogs.count(),
    "total_views" : blogs.aggregate(Sum('views'))['views__sum'] or 0,
    "published_blogs": blogs.filter(published=True).count(),
    "queued_blogs": blogs.filter(queued=True, published=False).count(),
    "reverted_blogs": blogs.filter(revert=True, published=False, queued=False).count(),
    "draft_blogs": blogs.filter(published=False, queued=False, revert=False).count(),
    "queued_list": blogs.filter(queued=True, published=False),
    "reverted_list": blogs.filter(revert=True, published=False, queued=False),
    "draft_list": blogs.filter(published=False, queued=False, revert=False),
    "dashboard": logincheck(request),
    "blogs": blogs.filter(published=True),
    "no_social": True,
  }
  return render(request, 'accounts/dashboard.html', context)

def logincheck(request):
  username = str(request.user)
  if username != 'AnonymousUser':
    return True
  else:
    return False

def forgot_password(request):
  mail_success = False
  user_not_exist = False
  if request.method == "POST":
    email = request.POST.get("email")
    try:
      user = User.objects.get(email=email)

      # Generate password reset token
      token = default_token_generator.make_token(user)
      uid = urlsafe_base64_encode(force_bytes(user.pk))
      reset_link = f"http://{request.get_host()}/accounts/reset-password/{uid}/{token}/"

      # Send email
      subject = "Reset Your Password"
      message = render_to_string("accounts/password_reset_email.html", {
        "user": user,
        "reset_link": reset_link
      })

      # Strip HTML tags for a plain text version
      plain_message = strip_tags(message)

      email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,  # Plain text message for email clients that don't support HTML
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
      )
      email.attach_alternative(message, "text/html")  # Attach HTML version
      email.send()

      mail_success = True

    except User.DoesNotExist:
      user_not_exist = True

  return render(request, "accounts/forgot_password.html", {"mail_sent": mail_success,
                                                           "user_not_exist": user_not_exist})

def reset_password(request, uidb64, token):
  errors = ""
  success = False
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    if not default_token_generator.check_token(user, token):
      return render(request, "accounts/invalid_verification.html")

  except (User.DoesNotExist, ValueError, TypeError):
    return render(request, "accounts/invalid_verification.html")

  if request.method == "POST":
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")

    if password1 != password2:
      errors = "Passwords do not match."
    elif len(password1) < 6:
      errors = "Password must be at least 6 characters long."
    else:
      user.set_password(password1)
      user.save()
      success = True

  return render(request, "accounts/reset_password.html", {'errors': errors, 'success': success})