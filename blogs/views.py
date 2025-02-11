from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache
from .models import Blog, Subscribe, service, suggestions, BlogView
from .utils import subscribe, get_client_ip, categorize_blogs, handle_subscription, is_bot
import random
import time

# Index Page
def index(request):
    """ Renders the homepage with cached blog data """
    all_blogs = cache.get('blog_list')
    if not all_blogs:
        blogs_queryset = Blog.objects.filter(published=True).order_by('-pk')
        sponsored_main = list(Blog.objects.filter(sponsored=True, show_blog_at='Main', published=True).order_by('-pk'))
        sponsored_side = list(Blog.objects.filter(sponsored=True, show_blog_at='Side', published=True).order_by('-pk'))
        unsponsored = list(Blog.objects.filter(sponsored=False, published=True).order_by('-pk'))
        all_blogs = sponsored_main + sponsored_side + unsponsored if sponsored_main or sponsored_side else blogs_queryset
        cache.set('blog_list', all_blogs, timeout=3600)  # Cache for 1 hour

    main_blog, recent, blogs = categorize_blogs(all_blogs)
    submission, subscribed = handle_subscription(request)

    # Handle Search Query
    search_title = request.GET.get('search')
    if search_title:
        search_result = Blog.objects.filter(Title=search_title, published=True).first()
        if search_result:
            return redirect(f'/blog/{search_result.url}')

    return render(request, 'index.html', {
        'main': main_blog, 'recent': recent, 'blogs': blogs,
        'category': False, 'submission': submission, 'subscribed': subscribed
    })

# Blog Detail Page
def blog(request, url):
    """ Handles individual blog page views with caching and rate-limited view counting """
    cache_key = f'blog_{url}'
    try:
        blog_post = cache.get(cache_key)
    except:
        blog_post = None
    if blog_post is None:
        blog_post = get_object_or_404(Blog, url=url, published=True)
        cache.set(cache_key, blog_post, timeout=3600)  # Cache blog content for 1 hour

    user_ip = get_client_ip(request)
    last_visit = request.session.get(f'blog_view_{blog_post.id}')
    current_time = time.time()

    # Rate-limit view counting (1 view per 60 seconds per user)
    if not last_visit or (current_time - last_visit) >= 60:
        request.session[f'blog_view_{blog_post.id}'] = current_time  # Update session timestamp
        if not is_bot(request):
            if not BlogView.objects.filter(blog=blog_post, ip_address=user_ip).exists():
                BlogView.objects.create(blog=blog_post, ip_address=user_ip)
                blog_post.views += 1
                blog_post.save(update_fields=['views'])

    related_blogs = list(Blog.objects.filter(category=blog_post.category, published=True).exclude(pk=blog_post.pk))
    random.shuffle(related_blogs)
    related_blogs = related_blogs[:3]  # Select 3 random related blogs

    submission, subscribed = handle_subscription(request)
    return render(request, 'Blogs.html', {
        'content': [blog_post], 'description': blog_post.meta_description, 'toc': blog_post.table_of_content,
        'submission': submission, 'subscribed': subscribed, 'blogs': related_blogs,
        'category': blog_post.category, 'title': blog_post.Title, 'url': blog_post.url,
        'sponsored': blog_post.sponsored, 'nofollow': blog_post.nofollow, 'dofollow': blog_post.dofollow,
        'noreferrer': blog_post.noreferrer, 'noopener': blog_post.noopener
    })

# Category Page
def categories(request, category):
    """ Displays blogs from a specific category """
    cache_key = f'category_{category}'
    blogs_queryset = cache.get(cache_key)

    if not blogs_queryset:
        blogs_queryset = Blog.objects.filter(category=category, published=True).order_by('-pk')
        cache.set(cache_key, blogs_queryset, timeout=3600)

    main_blog, recent, blogs = categorize_blogs(blogs_queryset)
    submission, subscribed = handle_subscription(request)

    return render(request, 'index.html', {
        'main': main_blog, 'recent': recent, 'blogs': blogs,
        'category': True, 'submission': submission, 'subscribed': subscribed
    })

# Blog Search API
def get_blog(request):
    """ Returns cached blog titles for search autocomplete """
    search = request.GET.get('search')
    cached_titles = cache.get('blog_titles')

    if not cached_titles:
        cached_titles = list(Blog.objects.filter(published=True).values_list('Title', flat=True))
        cache.set('blog_titles', cached_titles, timeout=86400)  # Store for 1 day

    return JsonResponse({'status': True, 'payload': cached_titles})

# Offer Page
def offer(request):
    """ Handles service requests """
    if request.method == "POST" and request.POST.get("service") == 'service':
        service.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )
        return redirect('/thankyou?offer=offer')

    submission, subscribed = handle_subscription(request)
    return render(request, 'offer.html', {'submission': submission, 'subscribed': subscribed})

# About Us Page
def aboutus(request):
    submission, subscribed = handle_subscription(request)
    return render(request, 'aboutus.html', {'submission': submission, 'subscribed': subscribed})

# Suggestion Page
def suggestion(request):
    """ Handles user suggestions """
    if request.method == "POST" and request.POST.get("suggestions") == 'suggestions':
        suggestions.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            suggestion=request.POST.get('suggestion')
        )
        return redirect('/thankyou?suggestion=suggestion')

    submission, subscribed = handle_subscription(request)
    return render(request, 'suggestion.html', {'submission': submission, 'subscribed': subscribed})

# Thank You Page
def thankyou(request):
    """ Displays a thank-you message after submission """
    heading = 'Interest' if request.GET.get('offer') else 'Suggestion'
    para = ("We appreciate your interest in The Circular Tribe and our mission to promote sustainability."
            if request.GET.get('offer')
            else "We appreciate your input and will review your suggestion carefully.")
    return render(request, 'thankyou.html', {'heading': heading, 'para': para})

# Static Pages
def terms_and_condition(request):
    submission, subscribed = handle_subscription(request)
    return render(request, 'terms-and-condition.html', {'submission': submission, 'subscribed': subscribed})


def privacy_policy(request):
    submission, subscribed = handle_subscription(request)
    return render(request, 'privacy-policy.html', {'submission': submission, 'subscribed': subscribed})


def cookie_policy(request):
    submission, subscribed = handle_subscription(request)
    return render(request, 'cookie-policy.html', {'submission': submission, 'subscribed': subscribed})


# Error Pages
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def server_error(request, exception=None):
    return render(request, '500.html', status=500)
