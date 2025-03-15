from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # Extra field example
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resend_attempts = models.IntegerField(default=0)
    last_resend_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username