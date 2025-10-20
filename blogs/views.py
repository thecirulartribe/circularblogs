from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommunityApplicationForm
from django.http import JsonResponse
from django.core.cache import cache
from .models import Blog, service, suggestions, BlogView
from .utils import get_client_ip, categorize_blogs, handle_subscription, is_bot, url_creater
from django.core.paginator import Paginator
import random
import time
from accounts.models import CustomUser

# Index Page
def index(request):
  """ Renders the homepage with cached blog data """
  all_blogs = cache.get('blog_list')
  main_blog, recent, blogs = {}, {}, {}
  if not all_blogs:
    # Use separate optimized queries instead of filtering in Python
    sponsored_main = list(Blog.objects.select_related('author_user').filter(
      published=True, sponsored=True, show_blog_at='Main'
    ).order_by('-pk'))

    sponsored_side = list(Blog.objects.select_related('author_user').filter(
      published=True, sponsored=True, show_blog_at='Side'
    ).order_by('-pk'))

    remaining = list(Blog.objects.select_related('author_user').filter(
      published=True
    ).exclude(
      sponsored=True, show_blog_at__in=['Main', 'Side']
    ).order_by('-pk'))

    if sponsored_main:
      all_blogs = sponsored_main + sponsored_side + remaining
    else:
      head = remaining[:1]
      tail = remaining[1:]
      all_blogs = head + sponsored_side + tail
    cache.set('blog_list', all_blogs, timeout=3600)  # Cache for 1 hour

  # Implement pagination
  paginator = Paginator(all_blogs, 12)  # Show 10 blogs per page
  page_number = request.GET.get("page")
  page_blog = paginator.get_page(page_number)

  if not page_number or int(page_number) == 1:
    main_blog, recent, blogs = categorize_blogs(page_blog)
  else:
    blogs = page_blog

  # Handle Search Query
  search_title = request.GET.get('search')
  if search_title:
    search_result = Blog.objects.filter(Title=search_title, published=True).first()
    if search_result:
      return redirect(f'/blog/{search_result.url}')

  submission, subscribed = handle_subscription(request)
  return render(request, 'index.html', {
    'main': main_blog, 'recent': recent, 'blogs': blogs,
    'category': False, 'page_blog': page_blog,
    'submission': submission, 'subscribed': subscribed
  })

# Blog Detail Page
def blog(request, url):
  """ Handles individual blog page views with caching and rate-limited view counting """
  cache_key = f'blog_{url}'
  blog_post = cache.get(cache_key)
  if blog_post is None:
    blog_post = get_object_or_404(Blog.objects.select_related('author_user'), url=url, published=True)
    cache.set(cache_key, blog_post, timeout=3600)  # Cache blog content for 1 hour

  user_ip = get_client_ip(request)
  last_visit = request.session.get(f'blog_view_{blog_post.id}')
  current_time = time.time()

  # Rate-limit view counting (1 view per 60 seconds per user)
  if not last_visit or (current_time - last_visit) >= 60:
    request.session[f'blog_view_{blog_post.id}'] = current_time  # Update session timestamp
    if not is_bot(request):
      # Use get_or_create to avoid duplicate check
      blog_view, created = BlogView.objects.get_or_create(
        blog=blog_post,
        ip_address=user_ip
      )
      if created:
        # Use F() expression to avoid race conditions
        from django.db.models import F
        Blog.objects.filter(pk=blog_post.pk).update(views=F('views') + 1)

  # Author is already loaded via select_related
  if blog_post.author_user:
    author_name = blog_post.author_user
  else:
    author_name = {
      "first_name": "Tribal",
      "last_name": "member"
    }

  # Cache related blogs separately and limit query
  related_cache_key = f'related_blogs_{blog_post.category}_{blog_post.pk}'
  related_blogs = cache.get(related_cache_key)
  if related_blogs is None:
    related_blogs = list(Blog.objects.filter(
      category=blog_post.category,
      published=True
    ).exclude(pk=blog_post.pk).order_by('?')[:3])  # Use database randomization
    cache.set(related_cache_key, related_blogs, timeout=1800)  # 30 min cache
  submission, subscribed = handle_subscription(request)
  return render(request, 'Blogs.html', {
    'content': [blog_post], 'description': blog_post.meta_description, 'toc': blog_post.table_of_content,
    'blogs': related_blogs, 'category': blog_post.category, 'title': blog_post.Title, 'url': blog_post.url,
    'sponsored': blog_post.sponsored, 'nofollow': blog_post.nofollow, 'dofollow': blog_post.dofollow,
    'noreferrer': blog_post.noreferrer, 'noopener': blog_post.noopener, 'author' : author_name,
    'submission': submission, 'subscribed': subscribed
  })

# Category Page
def categories(request, category):
  """ Displays blogs from a specific category """
  cache_key = f'category_{category}'
  blogs_queryset = cache.get(cache_key)

  if not blogs_queryset:
    blogs_queryset = Blog.objects.select_related('author_user').filter(
      category=category, published=True
    ).order_by('-pk')
    cache.set(cache_key, blogs_queryset, timeout=3600)

  paginator = Paginator(blogs_queryset, 12)  # Show 10 blogs per page
  page_number = request.GET.get("page")
  page_blog = paginator.get_page(page_number)

  main_blog, recent, blogs = categorize_blogs(page_blog)
  submission, subscribed = handle_subscription(request)
  return render(request, 'categories.html', {
    'main': main_blog, 'recent': recent, 'blogs': blogs, 'page_blog': page_blog,
    'category': category,
  'submission':submission, 'subscribed': subscribed})

# Blog Search API
def get_blog(request):
  """ Returns cached blog titles for search autocomplete """
  search = request.GET.get('search', '').strip()
  if not search or len(search) < 3:
    return JsonResponse({'status': True, 'payload': []})

  cache_key = f'search_{search.lower()}'
  payload = cache.get(cache_key)
  if payload is None:
    payload = list(Blog.objects.filter(
      Title__icontains=search, published=True
    ).values_list('Title', flat=True)[:10])  # Limit results
    cache.set(cache_key, payload, timeout=900)  # 15 min cache
  return JsonResponse({'status': True, 'payload': payload})

# Offer Page
def offer(request):
  """ Displays collaboration information page """
  submission, subscribed = handle_subscription(request)
  return render(request, 'offer.html', {'submission': submission, 'subscribed': subscribed})

# About Us Page
def aboutus(request):
  submission, subscribed = handle_subscription(request)
  return render(request, 'aboutus.html', {'submission': submission, 'subscribed': subscribed})

# Suggestion Page
def suggestion(request):
  """ Handles user feedback and suggestions """
  if request.method == "POST" and request.POST.get("suggestions") == 'suggestions':
    suggestions.objects.create(
      name=request.POST.get('name', ''),
      email=request.POST.get('email', ''),
      topic=request.POST.get('topic', 'Feedback'),
      suggestion=request.POST.get('suggestion')
    )
    return redirect('/thankyou?suggestion=suggestion')
  submission, subscribed = handle_subscription(request)
  return render(request, 'suggestion.html', {'submission': submission, 'subscribed': subscribed})

def write_for_us(request):
  """ Handles write for us community applications """
  form = CommunityApplicationForm()

  if request.method == "POST" and request.POST.get("community_application") == 'community_application':
    form = CommunityApplicationForm(request.POST)

    if form.is_valid():
      email = form.cleaned_data['email']

      # Check if user already exists with this email
      if service.objects.filter(email=email).exists():
        form.add_error('email', 'An application with this email address already exists. Please use a different email or contact us if you need assistance.')
        submission, subscribed = handle_subscription(request)
        return render(request, 'write-for-us.html', {
          'form': form,
          'submission': submission,
          'subscribed': subscribed
        })

      # Save the application
      form.save()

      return redirect('/thankyou?community=community')

  submission, subscribed = handle_subscription(request)
  return render(request, 'write-for-us.html', {
    'form': form,
    'submission': submission,
    'subscribed': subscribed
  })

# Thank You Page
def thankyou(request):
  """ Displays a thank-you message after submission """
  if request.GET.get('community'):
    heading = 'Application Received!'
    para = "Thank you for applying to join CircularBlogs community! We've received your application and will review it carefully. Check your email for confirmation and next steps."
  else:
    heading = 'Suggestion'
    para = "We appreciate your input and will review your suggestion carefully."
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

'''
@login_required
def create_blog_view(request):
  if request.method == "POST":
    form = BlogForm(request.POST, request.FILES)  # Ensure file uploads work
    if form.is_valid():
      user_blog = form.save(commit=False)  # Don't save yet
      if not user_blog.author_user:  # Only assign if the author isn't already set
        user_blog.author_user = request.user
      if user_blog.queued:
        user_blog.url = url_creater(f"{user_edited_blog.Title} {user_blog.author_user}")
      user_blog.save()  # Save now
      return redirect("/accounts/dashboard/")  # Redirect to your blog list page
  else:
    form = BlogForm()
  return render(request, "accounts/edit_blog.html", {"form": form, 'dashboard': True, 'page_title': "Create Blog"})

@login_required
def edit_blog_view(request, blog_id):
  user_blog = Blog.objects.get(id=blog_id)

  if user_blog.author_user != request.user:  # Prevent unauthorized editing
    return redirect("/accounts/dashboard/")  # Redirect if not the owner
  if user_blog.published:
    return redirect("/accounts/dashboard/")

  if request.method == "POST":
    form = BlogForm(request.POST, request.FILES, instance=user_blog)
    user_edited_blog = form.save(commit=False)
    if form.is_valid():
      if user_edited_blog.queued:
        user_edited_blog.url = url_creater(f"{user_edited_blog.Title} by {user_blog.author_user}")
      form.save()
      return redirect("/accounts/dashboard/")  # Change to your blog list view
  else:
    form = BlogForm(instance=user_blog)
  return render(request, "accounts/edit_blog.html", {"form": form, 'dashboard': True, 'page_title': "Edit Blog"})

@login_required
def delete_blog_view(request, blog_id):
  user_blog = get_object_or_404(Blog, id=blog_id, author_user=request.user)
  if request.method == 'POST':
    user_blog.delete()
    return redirect('/accounts/dashboard/')
  return render(request, 'blog/delete_blog.html', {'blog': user_blog, 'dashboard': True})
'''
