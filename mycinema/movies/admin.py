from django.contrib import admin

from .models import Movie


# class MovieAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'movie_id', 'name', 'genre', 'description', 'trailer_link', 'duration', 'price', 'date_added',
#         'is_published')
#     list_display_links = ('id', 'name')
#     list_filter = ('name',)
#     list_editable = ('is_published',)
#     search_fields = (
#         'id', 'movie_id', 'name', 'genre', 'description', 'trailer_link', 'duration', 'price', 'date_added',
#         'is_published')
#     list_per_page = 25


class MovieAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'name', 'image_tag', 'price', 'duration', 'delete', 'modify')
    list_display_links = ('id', 'name')
    list_filter = ()
    list_editable = ()
    # list_per_page = 25


admin.site.register(Movie, MovieAdmin)
