from django.contrib import admin

from .models import CinemaRoom


# class CinemaRoomAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'row_sits', 'column_sits', 'is_published')
#     list_display_links = ('id', 'name')
#     list_filter = ('name',)
#     list_filter = ()
#     list_editable = ('is_published',)
#     search_fields = ('id', 'name', 'row_sits', 'column_sits', 'is_published')
#     list_per_page = 25

class CinemaRoomAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'name', 'image_tag', 'delete', 'modify')
    list_display_links = ('id', 'name')
    list_filter = ()
    list_editable = ()
    search_fields = ()

admin.site.register(CinemaRoom, CinemaRoomAdmin)
