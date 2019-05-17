from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'photo', 'phone_number', 'birthdate', 'user_id')
    list_display_links = ('id', 'user_id')
    # list_filter = ('birthdate',)
    list_filter = ()
    list_editable = ('photo', 'phone_number', 'birthdate')
    search_fields = (
        'id', 'photo', 'phone_number', 'birthdate', 'user_id__username')
    list_per_page = 25


admin.site.register(Profile, ProfileAdmin)
