from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Blog(models.Model):
    Title = models.CharField(max_length=100)
    image = models.ImageField()
    content = CKEditor5Field(config_name='extends', blank=True, null=True)
    category = models.CharField(default=('Others', 'Others'), max_length=20,
                                choices=[('Environment', 'Environment'), ('Technology', 'Technology'),
                                         ('Agriculture', 'Agriculture'), ('Life-style', 'Life-style'),
                                         ('Fashion', 'Fashion'), ('Food', 'Food'), ('Education', 'Education'),
                                         ('DIY', 'DIY'), ('News', 'News'), ('Travel', 'Travel'),
                                         ('Case-Studies', 'Case-Studies'), ('Others', 'Others')])
    blog_date = models.DateTimeField(auto_now_add=True)
    meta_description = models.CharField(default="description", max_length=300)
    author = models.CharField(default=('Shreyash', 'Shreyash'), max_length=10, choices=[('Shreyash', 'Shreyash'), ('Tanmay', 'Tanmay'), ('Prathmesh', 'Prathmesh')])
    sponsered = models.BooleanField(default=False)
    show_blog_at = models.CharField(default=('None', 'None'), max_length=20, choices=[('None', 'None'), ('Main', 'Main'), ('Side', 'Side')])
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.Title + " | " + self.author


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
