from django.db import models

from .category import Category

class Post(models.Model):
    rareuser = models.ForeignKey("rareapi.rareuser", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="categories")
    title = models.CharField(max_length=55)
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=1000)
    content = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)