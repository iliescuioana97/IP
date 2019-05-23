from django.db import models
from django.utils.safestring import mark_safe


class CinemaRoom(models.Model):
    name = models.CharField(max_length=200)
    photo_main = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', max_length=255)
    photo_1 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True, max_length=255)
    photo_2 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True, max_length=255)
    photo_3 = models.ImageField(upload_to='photos/rooms/%Y/%m/%d/', blank=True, max_length=255)
    row_sits = models.IntegerField(default=13)
    column_sits = models.IntegerField(default=7)
    is_published = models.BooleanField(default=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="100" />' % (self.photo_main))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name
