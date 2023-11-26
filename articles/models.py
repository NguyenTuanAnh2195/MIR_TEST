from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=256, default="")
    title_slug = models.SlugField(null=True, blank=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        if self.is_published:
            self.publication_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_slug


class ContactRequest(models.Model):
    email = models.EmailField(null=False, blank=False)
    name = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
