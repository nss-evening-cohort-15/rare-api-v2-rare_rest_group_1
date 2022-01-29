from pickle import TRUE
from django.db import models

from django.contrib.auth.models import User

class RareUser(models.Model):
    bio = models.CharField(max_length=500, null=TRUE)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)