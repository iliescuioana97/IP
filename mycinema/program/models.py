from django.db import models
from django.forms import forms

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

    def __str__(self):
        return self.movie_id.name


class Ticket(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    show_id = models.ForeignKey(Show, on_delete=models.DO_NOTHING)
    row_num = models.IntegerField()
    col_num = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return "{}_{}".format(self.show_id.movie_id.name, self.user_id.username)
