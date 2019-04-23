# Generated by Django 2.2 on 2019-04-23 22:50

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('genre', models.CharField(blank=True, max_length=200)),
                ('description', models.CharField(blank=True, max_length=2000)),
                ('trailer_link', models.CharField(blank=True, max_length=200)),
                ('duration', models.IntegerField(blank=True, default=3600)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('photo_main', models.ImageField(upload_to='photos/movies/%Y/%m/%d/')),
                ('date_added', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]
