from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
  class Meta:
    model = Blog
    fields = ("Title", "image", "table_of_content", "content", "category", "queued")

    widgets = {
      "table_of_content": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
      "queued": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
    }

    errors = {
      "url": {"required": "The blog URL is required."},
      "Title": {"required": "Please enter a title for your blog."},
      "image": {"required": "An image is required for your blog."},
      "category": {"required": "Please select a category for your blog."},
      "content": {"required": "Content cannot be empty."},
    }

  def clean_Title(self):
    title = self.cleaned_data.get("Title")
    if len(title) < 5:
      raise forms.ValidationError("Title must be at least 5 characters long.")
    return title


class BlogEditForm(forms.ModelForm):
  class Meta:
    model = Blog
    fields = ("url", "Title", "image", "table_of_content", "content", "category", "queued")

    widgets = {
      "table_of_content": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
      "queued": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
    }

    errors = {
      "Title": {"required": "Please enter a title for your blog."},
      "image": {"required": "An image is required for your blog."},
      "category": {"required": "Please select a category for your blog."},
      "content": {"required": "Content cannot be empty."},
    }

  def clean_Title(self):
    title = self.cleaned_data.get("Title")
    if len(title) < 5:
      raise forms.ValidationError("Title must be at least 5 characters long.")
    return title

  def clean_url(self):
    url = self.cleaned_data.get("url")
    queued = self.cleaned_data.get("queued", False)

    if not queued:  # If the blog is still a draft
      return url  # Allow duplicate URLs for drafts

    # If it's ready for review, check uniqueness
    if Blog.objects.filter(url=url).exclude(id=self.instance.id).exists():
      raise forms.ValidationError("A blog with this URL already exists. Please use a different URL.")
    return url