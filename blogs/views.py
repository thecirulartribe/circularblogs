from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from django.http import JsonResponse
from django.core.cache import cache
from .models import Blog, Subscribe, service, suggestions, BlogView
from .utils import subscribe, get_client_ip, categorize_blogs, handle_subscription, is_bot, url_creater
from django.core.paginator import Paginator
import random
import time
from accounts.views import logincheck
from accounts.models import CustomUser

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

  # Implement pagination
  paginator = Paginator(all_blogs, 10)  # Show 10 blogs per page
  page_number = request.GET.get("page")
  page_blog = paginator.get_page(page_number)

  main_blog, recent, blogs = categorize_blogs(page_blog)

  # Handle Search Query
  search_title = request.GET.get('search')
  if search_title:
    search_result = Blog.objects.filter(Title=search_title, published=True).first()
    if search_result:
      return redirect(f'/blog/{search_result.url}')

  check = logincheck(request)
  return render(request, 'index.html', {
    'main': main_blog, 'recent': recent, 'blogs': blogs,
    'category': False, 'dashboard': check,  'page_blog': page_blog})

# Blog Detail Page
def blog(request, url):
  """ Handles individual blog page views with caching and rate-limited view counting """
  cache_key = f'blog_{url}'
  blog_post = cache.get(cache_key)
  if blog_post is None:
    blog_post = get_object_or_404(Blog, url=url, published=True)
    cache.set(cache_key, blog_post, timeout=3600)  # Cache blog content for 1 hour

  user_ip = get_client_ip(request)
  last_visit = request.session.get(f'blog_view_{blog_post.id}')
  current_time = time.time()
  check = logincheck(request)

  # Rate-limit view counting (1 view per 60 seconds per user)
  if not last_visit or (current_time - last_visit) >= 60:
    request.session[f'blog_view_{blog_post.id}'] = current_time  # Update session timestamp
    if not is_bot(request):
      if not BlogView.objects.filter(blog=blog_post, ip_address=user_ip).exists():
        BlogView.objects.create(blog=blog_post, ip_address=user_ip)
        blog_post.views += 1
        blog_post.save(update_fields=['views'])

  author_info = list(CustomUser.objects.filter(username=blog_post.author_user))
  related_blogs = list(Blog.objects.filter(category=blog_post.category, published=True).exclude(pk=blog_post.pk))
  random.shuffle(related_blogs)
  related_blogs = related_blogs[:3]  # Select 3 random related blogs

  return render(request, 'Blogs.html', {
    'content': [blog_post], 'description': blog_post.meta_description, 'toc': blog_post.table_of_content,
    'blogs': related_blogs, 'category': blog_post.category, 'title': blog_post.Title, 'url': blog_post.url,
    'sponsored': blog_post.sponsored, 'nofollow': blog_post.nofollow, 'dofollow': blog_post.dofollow,
    'noreferrer': blog_post.noreferrer, 'noopener': blog_post.noopener, 'dashboard': check, 'author' : author_info[0]
  })

# Category Page
def categories(request, category):
  """ Displays blogs from a specific category """
  cache_key = f'category_{category}'
  blogs_queryset = cache.get(cache_key)
  check = logincheck(request)

  if not blogs_queryset:
    blogs_queryset = Blog.objects.filter(category=category, published=True).order_by('-pk')
    cache.set(cache_key, blogs_queryset, timeout=3600)

  main_blog, recent, blogs = categorize_blogs(blogs_queryset)

  return render(request, 'index.html', {
    'main': main_blog, 'recent': recent, 'blogs': blogs,
    'category': True, 'dashboard': check })

# Blog Search API
def get_blog(request):
  """ Returns cached blog titles for search autocomplete """
  search = request.GET.get('search')
  payload = list(Blog.objects.filter(Title__icontains=search, published=True).values_list('Title', flat=True))
  return JsonResponse({'status': True, 'payload': payload})

# Offer Page
def offer(request):
  check = logincheck(request)

  """ Handles service requests """
  if request.method == "POST" and request.POST.get("service") == 'service':
    service.objects.create(
      name=request.POST.get("name"),
      email=request.POST.get("email"),
      message=request.POST.get("message")
    )
    return redirect('/thankyou?offer=offer')

  return render(request, 'offer.html', {'dashboard': check})

# About Us Page
def aboutus(request):
  check = logincheck(request)
  submission, subscribed = handle_subscription(request)
  return render(request, 'aboutus.html', {'dashboard': check, 'subcribe_form': True, 'submission': submission, 'subscribed': subscribed})

# Suggestion Page
def suggestion(request):
  check = logincheck(request)
  """ Handles user suggestions """
  if request.method == "POST" and request.POST.get("suggestions") == 'suggestions':
    suggestions.objects.create(
      name=request.POST.get('name'),
      email=request.POST.get('email'),
      suggestion=request.POST.get('suggestion')
    )
    return redirect('/thankyou?suggestion=suggestion')

  return render(request, 'suggestion.html', {'dashboard': check})

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
  check = logincheck(request)
  return render(request, 'terms-and-condition.html', {'dashboard': check})


def privacy_policy(request):
  check = logincheck(request)
  return render(request, 'privacy-policy.html', {'dashboard': check})


def cookie_policy(request):
  check = logincheck(request)
  return render(request, 'cookie-policy.html', {'dashboard': check})


# Error Pages
def page_not_found_view(request, exception):
  return render(request, '404.html', status=404)


def server_error(request, exception=None):
  return render(request, '500.html', status=500)


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
