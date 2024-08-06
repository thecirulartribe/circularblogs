from django.db import models
from time import time


# Create your models here.
class Blog(models.Model):
    Title = models.CharField(max_length=100)
    image = models.ImageField()
    content = models.TextField()
    category = models.CharField(default=('recent', 'recent'), max_length=20, choices=[('tech', 'technology'), ('soft', 'software'), ('renew', 'renewable'),
                                                                                      ('recycle', 'recyclable'), ('recent', 'recent')])
    blog_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title


class Subscribe(models.Model):
    name = models.CharField(default="No Name", max_length=100)
    email_id = models.EmailField()

    def __str__(self):
        return self.name
