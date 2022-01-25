from django.db import models

from django.contrib.auth.models import User

class RareUser(models.Model):
    bio = models.CharField(max_length=500)
    profile_image_url = models.URLField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    user_id = models.OneToOneField(User, on_delete=models.DO_NOTHING)