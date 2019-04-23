from django.db import models


class CinemaRoom(models.Model):
    name = models.CharField(max_length=200)
    photo_main = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True)
    row_sits = models.IntegerField(default=12)
    column_sits = models.IntegerField(default=12)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name
