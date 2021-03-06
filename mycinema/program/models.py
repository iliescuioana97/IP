from django.db import models
from django.forms import forms
from django.utils.safestring import mark_safe

from datetime import datetime

from django.contrib.auth.models import User

from movies.models import Movie
from cinema_rooms.models import CinemaRoom


class Show(models.Model):
    date = models.DateTimeField(default=datetime.now)
    hour_begin = models.TimeField()
    hour_end = models.TimeField()
    movie_id = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    room_id = models.ForeignKey(CinemaRoom, on_delete=models.DO_NOTHING)
    is_published = models.BooleanField(default=True)

    def modify(self):
        return mark_safe('<a href="/admin/program/show/%s/change/">Edit</a>' % (self.id))

    def delete(self):
        return mark_safe('<div class="delete-checkbox"></div>')

    def __str__(self):
        return "{}__{}".format(self.movie_id.name, self.date.strftime('%Y-%m-%d %H:%M:%S'))


class Ticket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    show_id = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    row_num = models.IntegerField()
    col_num = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)

    def modify(self):
        return mark_safe('<a href="/admin/program/ticket/%s/change/">Edit</a>' % (self.id))

    def delete(self):
        return mark_safe('<div class="delete-checkbox"></div>')

    def __str__(self):
        return "{}__{}".format(self.show_id.movie_id.name, self.user_id.username)
