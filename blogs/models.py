from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from django.core.cache import cache

# Create your models here.
class Blog(models.Model):
    url = models.CharField(max_length=100, blank=True, null=True)
    page_title = models.CharField(max_length=60, blank=True, null=True)
    Title = models.CharField(max_length=100)
    image = ResizedImageField(size=[950,300], quality=80, force_format='WEBP', crop=['middle', 'center'])
    table_of_content = models.BooleanField(default=False)
    content = CKEditor5Field(config_name='extends', blank=True, null=True)
    category = models.CharField(default=('Others', 'Others'), max_length=20,
                                choices=[('Environment', 'Environment'), ('Technology', 'Technology'),
                                         ('Agriculture', 'Agriculture'), ('Life-style', 'Life-style'),
                                         ('Fashion', 'Fashion'), ('Food', 'Food'), ('Education', 'Education'),
                                         ('DIY', 'DIY'), ('News', 'News'), ('Travel', 'Travel'),
                                         ('Case-Studies', 'Case-Studies'), ('Others', 'Others')])
    blog_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_description = models.CharField(default="description", max_length=300)
    author = models.CharField(default=('Shreyash', 'Shreyash'), max_length=10, choices=[('Shreyash', 'Shreyash'), ('Tanmay', 'Tanmay'), ('Prathmesh', 'Prathmesh')])
    sponsored = models.BooleanField(default=False)
    nofollow = models.BooleanField(default=False)
    dofollow = models.BooleanField(default=False)
    noreferrer = models.BooleanField(default=False)
    noopener = models.BooleanField(default=False)
    show_blog_at = models.CharField(default=('None', 'None'), max_length=20, choices=[('None', 'None'), ('Main', 'Main'), ('Side', 'Side')])
    published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)  # View counter

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('blog_list')  # Clear blog list cache
        cache.delete(f'blog_{self.url}')  # Clear specific blog cache

    def delete(self, *args, **kwargs):
        cache.delete('blog_list')
        cache.delete(f'blog_{self.url}')
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return f'/blog/{self.url}'


class Subscribe(models.Model):
    name = models.CharField(default="No Name", max_length=100)
    email_id = models.EmailField()

    def __str__(self):
        return self.name


class service(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class suggestions(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    suggestion = models.TextField()

    def __str__(self):
        return self.suggestion

class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_views')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog.Title} - {self.ip_address}"

class BotIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
