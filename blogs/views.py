from django.shortcuts import render
from .models import Blog, Subscribe


# Create your views here.
def index(request):
    content = Blog.objects.order_by('-pk')
    counter = 0
    main_blog = None
    recent = []
    blogs = []
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
        new_subscriber = Subscribe(name=Name, email_id=Email)
        new_subscriber.save()
    return render(request, 'index.html', {'main': main_blog, 'recent': recent, 'blogs': blogs})


def blog(request, title):
    content = Blog.objects.filter(Title=title)
    if request.method == "POST":
        Name = request.POST.get('Name')
        Email = request.POST.get('Email')
        new_subscriber = Subscribe(name=Name, email_id=Email)
        new_subscriber.save()
    return render(request, 'Blogs.html', {'content': content})


def offer(request):
    return render(request, 'offer.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def suggestion(request):
    return render(request, 'suggestion.html')
