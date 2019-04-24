import re

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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


@login_required(login_url='/accounts/login')
def save(request):
    if request.method == 'POST':
        photo = request.POST.get("profile_image")
        first_name = request.POST.get("settings_first_name")
        last_name = request.POST.get("settings_last_name")
        email = request.POST.get("settings_email")
        phone_number = request.POST.get("settings_phone_number")
        birthdate = request.POST.get("settings_birthdate")
        password1 = request.POST.get("settings_password1")
        password2 = request.POST.get("settings_password2")
        print("SALUT ")
        print(request.user.id)
        print(first_name)
        print(last_name)
        print(email)
        print(phone_number)
        print(birthdate)
        print(password1)
        print(password2)

        if first_name:
            first_name = first_name.strip()
            if not first_name:
                messages.error(request, 'First Name is not valid')
                return redirect('settings')

            User.objects.filter(id=request.user.id).update(first_name=first_name)

        if last_name:
            last_name = last_name.strip()
            if not last_name:
                messages.error(request, 'Last Name is not valid')
                return redirect('settings')

            User.objects.filter(id=request.user.id).update(last_name=last_name)

        if email:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                messages.error(request, 'Email is not valid')
                return redirect('settings')

            User.objects.filter(id=request.user.id).update(email=email)

        if password1 and password2:
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('settings')

            try:
                validate_password(password1)
            except Exception as e:
                messages.error(request, 'Password does not meet requirements')
                return redirect('settings')

        if phone_number:
            Profile.objects.filter(user_id=request.user.id).update(phone_number=phone_number)

        if birthdate:
            Profile.objects.filter(user_id=request.user.id).update(birthdate=birthdate)

        if photo:
            Profile.objects.filter(user_id=request.user.id).update(photo=photo)

        return render(request, 'settings/settings.html')
    else:
        return render(request, 'settings/settings.html')
