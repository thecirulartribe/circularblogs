from django import forms
from .models import Blog, service
from PIL import Image
import bleach


def validate_image(image):
  valid_extensions = ['.webp', '.jpeg', '.jpg', '.png']
  if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
    raise ValidationError('Unsupported file format!')

  # Ensure uploaded file has a proper size
  if image.size > 2 * 1024 * 1024:  # 2MB limit
    raise ValidationError('File size too large! Max 2MB allowed.')

  try:
    img = Image.open(image)
    img.verify()  # Check if it's a valid image

  except Exception:
    raise ValidationError('Invalid image file!')

class BlogForm(forms.ModelForm):
  image = forms.ImageField(validators=[validate_image])

  class Meta:
    model = Blog
    fields = ("Title", "image", "table_of_content", "content", "category", "queued")

    widgets = {
      "table_of_content": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
      "queued": forms.CheckboxInput(attrs={"class": "toggle-switch"}),
    }

    error_messages = {
      "url": {"required": "The blog URL is required."},
      "Title": {"required": "Please enter a title for your blog."},
      "image": {"required": "An image is required for your blog."},
      "category": {"required": "Please select a category for your blog."},
      "content": {"required": "Content cannot be empty."},
    }

  def clean_title(self):
    title = self.cleaned_data.get("title", "").strip()
    if not title:
      raise forms.ValidationError("Title is required.")
    if len(title) < 5:
      raise forms.ValidationError("Title must be at least 5 characters long.")
    return title

  def clean_content(self):
    content = self.cleaned_data.get("content").strip()

    if len(content) < 50:  # Ensure minimum meaningful content
      raise forms.ValidationError("Content must be at least 50 characters long.")

    allowed_tags = [
      'p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5',
      'blockquote', 'code', 'pre', 'img', 'table', 'tbody', 'tr', 'td', 'th', 'thead'
    ]
    allowed_attrs = {'a': ['href', 'title'], 'img': ['src', 'alt', 'width', 'height'], 'table': ['border']}
    cleaned_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    if cleaned_content.count(" ") < 10:  # Ensure sufficient text content
      raise forms.ValidationError("Content must have more meaningful text.")
    return cleaned_content

  def clean_category(self):
    category = self.cleaned_data.get("category")
    valid_categories = [choice[0] for choice in Blog._meta.get_field("category").choices]
    if category not in valid_categories:
      raise forms.ValidationError("Invalid category selected. Please choose a valid category.")
    return category


class CommunityApplicationForm(forms.ModelForm):
  class Meta:
    model = service
    fields = ['name', 'email', 'message']
    
    widgets = {
      'name': forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your full name',
        'required': True
      }),
      'email': forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your email address',
        'required': True
      }),
      'message': forms.Textarea(attrs={
        'class': 'form-input form-textarea',
        'rows': 6,
        'placeholder': 'Tell us about:\n• Your writing experience and expertise\n• Topics you\'re passionate about\n• Why you want to join our community\n• Any relevant background in sustainability/environment',
        'required': True
      })
    }
    
    error_messages = {
      'name': {'required': 'Please enter your full name.'},
      'email': {'required': 'Please enter a valid email address.'},
      'message': {'required': 'Please tell us about yourself.'}
    }
  
  def clean_name(self):
    name = self.cleaned_data.get('name', '').strip()
    if len(name) < 2:
      raise forms.ValidationError('Name must be at least 2 characters long.')
    return name
  
  def clean_message(self):
    message = self.cleaned_data.get('message', '').strip()
    if len(message) < 50:
      raise forms.ValidationError('Please provide more details about yourself (at least 50 characters).')
    return message