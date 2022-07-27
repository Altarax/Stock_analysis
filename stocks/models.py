from django.db import models


# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=60)
    symbol = models.CharField(max_length=10)
    slug = models.SlugField()
