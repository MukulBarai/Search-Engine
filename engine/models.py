from django.db import models

class Page(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    keywords = models.CharField(max_length=1000)
    crawled = models.IntegerField(default=0)
    broken = models.BooleanField(default=0)
    clicks = models.IntegerField(default=0)
    def __str__(self): return self.url


class Image(models.Model):
    url = models.CharField(max_length=500)
    src = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    alt = models.CharField(max_length=200)
    broken = models.BooleanField(default=0)
    clicks = models.IntegerField(default=0)
    def __str__(self): return self.src

