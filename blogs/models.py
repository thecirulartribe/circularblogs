from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django_resized import ResizedImageField
from django.core.cache import cache
from bs4 import BeautifulSoup

# Create your models here.
class Blog(models.Model):
  url = models.CharField(max_length=100, blank=True, null=True)
  author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
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
  sponsored = models.BooleanField(default=False)
  nofollow = models.BooleanField(default=False)
  dofollow = models.BooleanField(default=False)
  noreferrer = models.BooleanField(default=False)
  noopener = models.BooleanField(default=False)
  show_blog_at = models.CharField(default=('None', 'None'), max_length=20, choices=[('None', 'None'), ('Main', 'Main'), ('Side', 'Side')])
  published = models.BooleanField(default=False)
  queued = models.BooleanField(default=False)
  revert = models.BooleanField(default=False)
  views = models.PositiveIntegerField(default=0)
  read_time = models.PositiveIntegerField(default=5)

  def save(self, *args, **kwargs):
    self.calculate_read_time()
    super().save(*args, **kwargs)
    cache.delete('blog_list')  # Clear blog list cache
    cache.delete(f'blog_{self.url}')  # Clear specific blog cache

  def delete(self, *args, **kwargs):
    cache.delete('blog_list')
    cache.delete(f'blog_{self.url}')
    super().delete(*args, **kwargs)

  def get_absolute_url(self):
    return f'/blog/{self.url}'

  def calculate_read_time(self):
    content = self.content
    soup = BeautifulSoup(content, 'html.parser')
    txt_content = soup.get_text()
    word_count = len(txt_content.split())
    avg_read_speed = 200 #words/min
    read_time = int(word_count / avg_read_speed)
    self.read_time = read_time


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
  topic = models.CharField(max_length=50, choices=[
    ('Feedback', 'General Feedback'),
    ('Blog Idea', 'Blog Idea'),
    ('Collaboration', 'Collaboration Proposal')
  ], default='Feedback')
  suggestion = models.TextField()

  def __str__(self):
    return f"{self.topic}: {self.suggestion[:50]}..."

class BlogView(models.Model):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_views')
  ip_address = models.GenericIPAddressField()
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.blog.Title} - {self.ip_address}"

class BotIP(models.Model):
  ip_address = models.GenericIPAddressField(unique=True)
  added_on = models.DateTimeField(auto_now_add=True)
