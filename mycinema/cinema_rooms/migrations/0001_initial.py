# Generated by Django 2.2 on 2019-05-12 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo_main', models.ImageField(max_length=255, upload_to='photos/rooms/%Y/%m/%d/')),
                ('photo_1', models.ImageField(blank=True, max_length=255, upload_to='photos/rooms/%Y/%m/%d/')),
                ('photo_2', models.ImageField(blank=True, max_length=255, upload_to='photos/rooms/%Y/%m/%d/')),
                ('photo_3', models.ImageField(blank=True, max_length=255, upload_to='photos/rooms/%Y/%m/%d/')),
                ('row_sits', models.IntegerField(default=12)),
                ('column_sits', models.IntegerField(default=12)),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]
