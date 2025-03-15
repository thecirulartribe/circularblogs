from .models import Subscribe, BotIP
from .variables import BOT_USER_AGENTS
import re

def categorize_blogs(queryset):
    """Categorize blogs into main, recent, and blog sections."""
    queryset = list(queryset)  # Convert once to a list
    return (
        queryset[0] if queryset else None,  # Main blog
        queryset[1:4],  # Recent blogs (next 3)
        queryset[4:]  # Remaining blogs
    )

def handle_subscription(request):
    """Handles subscription form submissions."""
    if request.method == "POST":
        name = request.POST.get('Name', '').strip()
        email = request.POST.get('Email', '').strip().lower()  # Normalize once
        return bool(name and email), subscribe(name, email)
    return False, True  # Default values when no subscription occurs

def subscribe(name, email):
    """Subscribe a user if not already subscribed."""
    if not email or not name:  # Ensure valid inputs
        return False
    _, created = Subscribe.objects.get_or_create(email_id=email, defaults={"name": name})
    return created  # Returns True if newly created, False if it existed

def get_client_ip(request):
    """Retrieve the real IP address of the client."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return x_forwarded_for.partition(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def is_bot(request):
    """Check if the request comes from a bot using User-Agent and IP."""
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_ip = get_client_ip(request)

    # Check if User-Agent contains bot keywords (faster lookup using any() with "in")
    if any(bot in user_agent.lower() for bot in BOT_USER_AGENTS):
        _, created = BotIP.objects.get_or_create(ip_address=user_ip)
        return True

    # Directly check if the IP is already stored
    return BotIP.objects.filter(ip_address=user_ip).exists()


def url_creater(title):
    # Convert to lowercase
    title = title.lower()

    # Replace non-alphanumeric characters with spaces
    title = re.sub(r'[^a-z0-9\s]', '', title)

    # Replace multiple spaces with a single hyphen
    title = re.sub(r'\s+', '-', title)

    # Strip hyphens from start and end
    title = title.strip('-')

    return title
