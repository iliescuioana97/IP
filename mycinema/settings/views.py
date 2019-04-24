from django.shortcuts import render, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required
from django.apps import apps

Profile = apps.get_model('accounts', 'Profile')


@login_required(login_url='/accounts/login')
def index(request):
    user = request.user
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = None

    user_data = {
        "user_user_type": "administrator" if user.is_superuser else "mycinema user",
    }

    if profile:
        if profile.birthdate:
            user_data["user_birthdate"] = profile.birthdate
        if profile.phone_number:
            if "None" not in str(profile.phone_number):
                user_data["user_phone_number"] = profile.phone_number
        if profile.photo:
            user_data["user_avatar"] = profile.photo

    return render(request, 'settings/settings.html', user_data)
