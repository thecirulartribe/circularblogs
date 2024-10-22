from django.shortcuts import render, redirect
from .models import Blog, Subscribe, service, suggestions
from django.http import JsonResponse
import random

# Create your views here.
def index(request):
    content = Blog.objects.filter(published=True).order_by('-pk')
    sponsered = Blog.objects.filter(published=True,sponsered=True)
    counter = 0
    main_blog = None
    recent = []
    blogs = []
    submission = False
    subscribed = True
    if len(sponsered) > 0:
        sponsered_main = Blog.objects.filter(sponsered=True, show_blog_at='Main', published=True).order_by('-pk')
        sponsered_side = Blog.objects.filter(sponsered=True, show_blog_at='Side', published=True).order_by('-pk')
        unsponsered = Blog.objects.filter(sponsered=False, published=True).order_by('-pk')
        for data in sponsered_main:
            if counter == 0:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
        for data in sponsered_side:
            if counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
        for data in unsponsered:
            if main_blog is None:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
    else:
        for data in content:
            if counter == 0:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    if request.method == "GET":
        title = request.GET.get('search')
        content = Blog.objects.filter(Title=title,published=True)
        if len(content) != 0:
            return redirect(f'/blog/{content[0].url}')
    return render(request, 'index.html', {'main': main_blog, 'recent': recent, 'blogs': blogs, 'category': False, 'submission': submission, 'subscribed': subscribed})


def blog(request, url):
    content = Blog.objects.filter(url=url,published=True)
    title = content[0].Title
    url = content[0].url
    description = content[0].meta_description
    category = content[0].category
    cards_content = Blog.objects.filter(category=category, published=True).exclude(Title=title)
    submission = False
    subscribed = True
    counter = 3
    blogs = []
    cards_content = list(cards_content)
    random.shuffle(cards_content)
    for data in cards_content:
        if counter == 0:
            break
        else:
            blogs.append(data)
            counter -= 1
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'Blogs.html', {'content': content, 'description': description, 'submission': submission, 'subscribed': subscribed, 'blogs': blogs, 'category': category, 'title': title, 'url': url})


def categories(request, category):
    content = Blog.objects.filter(category=category, published=True).order_by('-pk')
    sponsered = Blog.objects.filter(category=category, sponsered=True, published=True)
    counter = 0
    main_blog = None
    recent = []
    blogs = []
    submission = False
    subscribed = True
    if len(sponsered) > 0:
        sponsered_main = Blog.objects.filter(category=category, sponsered=True, show_blog_at='Main', published=True).order_by('-pk')
        sponsered_side = Blog.objects.filter(category=category, sponsered=True, show_blog_at='Side', published=True).order_by('-pk')
        unsponsered = Blog.objects.filter(category=category, sponsered=False, published=True).order_by('-pk')
        for data in sponsered_main:
            if counter == 0:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
        for data in sponsered_side:
            if counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
        for data in unsponsered:
            if main_blog is None:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
    else:
        for data in content:
            if counter == 0:
                main_blog = data
            elif counter <= 3:
                recent.append(data)
            else:
                blogs.append(data)
            counter += 1
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    if request.method == "GET":
        title = request.GET.get('search')
        content = Blog.objects.filter(Title=title,published=True)
        if len(content) != 0:
            return redirect(f'/blog/{content[0].url}')
    return render(request, 'index.html', {'main': main_blog, 'recent': recent, 'blogs': blogs, 'category': True, 'submission': submission, 'subscribed': subscribed})


def offer(request):
    submission = False
    subscribed = True
    if request.method == "POST" and request.POST.get("service") == 'service':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        service_req = service(name=name, email=email, message=message)
        service_req.save()
        return redirect('/thankyou?offer=offer')
    elif request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'offer.html', {'submission': submission, 'subscribed': subscribed})


def aboutus(request):
    submission = False
    subscribed = True
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'aboutus.html', {'submission': submission, 'subscribed': subscribed})


def suggestion(request):
    submission = False
    subscribed = True
    if request.method == "POST" and request.POST.get("suggestions") == 'suggestions':
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        suggestion_given = request.POST.get('suggestion')
        suggested = suggestions(name=Name, email=Email, suggestion=suggestion_given)
        suggested.save()
        return redirect('/thankyou?suggestion=suggestion')
    elif request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'suggestion.html', {'submission': submission, 'subscribed': subscribed})


def get_blog(request):
    search = request.GET.get('search')
    objs = Blog.objects.filter(Title__icontains=search, published=True)
    payload = []
    for obj in objs:
        payload.append(obj.Title)
    return JsonResponse({
        'status': True,
        'payload': payload,
    })


def subscribe(name, email):
    if not already_subscribed(email):
        new_subscriber = Subscribe(name=name, email_id=email)
        new_subscriber.save()
        return True
    return False


def already_subscribed(email):
    subscriber = Subscribe.objects.filter(email_id=email)
    if len(subscriber) > 0:
        return True
    return False


def thankyou(request):
    if request.GET.get('offer'):
        heading = 'Interest'
        para = "We appreciate your interest in The Circular Tribe and our mission to promote sustainability. Our team is reviewing your message and will get back to you shortly with the information or assistance you need. In the meantime, feel free to explore our latest blog posts, discover sustainable brands, or connect with like-minded individuals in our community."
    else:
        heading = 'Suggestion'
        para = "We appreciate your input and will review your suggestion carefully. Your feedback helps us improve and grow. Together, we can make a difference."
    return render(request, 'thankyou.html', {'heading': heading, 'para': para})

def category_wise_count(request):
    category_list = ['Environment','Technology','Agriculture','Life-style', 'Fashion', 'Food', 'Education', 'DIY', 
                     'News', 'Travel', 'Case-Studies', 'Others']
    count = {}
    for category in category_list:
        blogs = Blog.objects.filter(category=category, published=True)
        count[category] = blogs.count()
    return render(request, 'category_list.html', {'count': count})

def terms_and_condition(request):
    submission = False
    subscribed = True
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'terms-and-condition.html', {'submission': submission, 'subscribed': subscribed})

def privacy_policy(request):
    submission = False
    subscribed = True
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        submission = True
        subscribed = subscribe(Name, Email)
    return render(request, 'privacy-policy.html', {'submission': submission, 'subscribed': subscribed})