from django.db import models

from datetime import datetime
import uuid


class Movie(models.Model):
    movie_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=2000, blank=True)
    trailer_link = models.CharField(max_length=200, blank=True)
    duration = models.IntegerField(default=3600, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo_main = models.ImageField(upload_to='photos/movies/%Y/%m/%d/')
    date_added = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name
