# blog/forms.py
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # Include fields you want to allow editing
        fields = ['url', 'Title', 'image', 'content', 'table_of_content', 'category']