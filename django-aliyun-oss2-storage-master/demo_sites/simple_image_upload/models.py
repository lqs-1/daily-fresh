from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Images(models.Model):
    image = models.ImageField(blank=False,
                              upload_to="image/%Y/%m/%d")
