from django.db import models

from .categories import Category

class Post(models.Model):
    user = models.CharField(max_length=55)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name="categories")
    title = models.CharField(max_length=55)
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=1000)
    content = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)