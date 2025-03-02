# blog/forms.py
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ["author_user", "sponsored", "nofollow", "dofollow", "noreferrer", "noopener", "show_blog_at", "views"]