from django.contrib import admin

from .models import Show, Ticket


class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'hour_begin', 'hour_end', 'movie_id', 'room_id', 'is_published')
    list_display_links = ('id', 'movie_id', 'room_id')
    list_filter = ('date', 'hour_begin', 'hour_end', 'room_id')
    list_editable = ('date', 'hour_begin', 'hour_end', 'is_published')
    search_fields = (
        'id', 'date', 'hour_begin', 'hour_end', 'movie_id__name', 'room_id__name', 'is_published'
    )
    list_per_page = 25


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'show_id', 'row_num', 'col_num', 'is_booked', 'is_valid')
    list_display_links = ('id',)
    list_filter = ('row_num', 'col_num', 'is_booked', 'is_valid')
    list_editable = ('user_id', 'show_id', 'row_num', 'col_num', 'is_booked', 'is_valid')
    search_fields = (
        'id', 'user_id__username', 'show_id__movie_id__name', 'row_num', 'col_num', 'is_booked', 'is_valid'
    )
    list_per_page = 25


admin.site.register(Show, ShowAdmin)
admin.site.register(Ticket, TicketAdmin)
