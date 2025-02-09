from .models import Subscribe, BotIP
from .variables import BOT_USER_AGENTS
import re

def categorize_blogs(queryset):
    """Categorize blogs into main, recent, and blog sections."""
    main_blog = queryset[0] if queryset else None
    recent = list(queryset[1:4])  # Next three blogs
    blogs = list(queryset[4:])  # Remaining blogs
    return main_blog, recent, blogs


def handle_subscription(request):
    """Handles subscription form submissions."""
    if request.method == "POST":
        name = request.POST.get('Name', '').strip()
        email = request.POST.get('Email', '').strip().lower()  # Normalize email
        if name and email:  # Ensure valid inputs
            return True, subscribe(name, email)
    return False, True  # Default values when no subscription occurs


def subscribe(name, email):
    """Subscribe a user if not already subscribed."""
    email = email.lower().strip()  # Normalize email input
    if not email or not name:  # Ensure name and email are provided
        return False  # Invalid subscription attempt
    if not Subscribe.objects.filter(email_id=email).exists():
        Subscribe.objects.create(name=name, email_id=email)
        return True  # Successfully subscribed
    return False  # Already subscribed


def get_client_ip(request):
    """Retrieve the real IP address of the client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_bot(request):
    """Check if the request comes from a bot using User-Agent and IP."""
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Check if User-Agent contains bot keywords
    if any(re.search(bot, user_agent, re.IGNORECASE) for bot in BOT_USER_AGENTS):
        return True

    # Check if the IP exists in the bot IP database
    user_ip = get_client_ip(request)
    if BotIP.objects.filter(ip_address=user_ip).exists():
        return True

    return False