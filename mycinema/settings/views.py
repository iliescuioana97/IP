import os
import re
from datetime import datetime

from PIL import Image

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.utils.timezone import localtime
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.password_validation import validate_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

Profile = apps.get_model('accounts', 'Profile')


def get_data(request):
    user = request.user
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = None

    user_data = {
        "user_user_type": "administrator" if user.is_superuser else "mycinema user",
        "user_first_name": user.first_name,
        "user_last_name": user.last_name,
        "user_email": user.email,
    }

    if profile:
        if profile.birthdate:
            user_data["user_birthdate"] = "{}/{}/{}".format(profile.birthdate.month, profile.birthdate.day,
                                                            profile.birthdate.year)
        if profile.phone_number:
            if "None" not in str(profile.phone_number):
                user_data["user_phone_number"] = profile.phone_number
        if profile.photo:
            user_data["user_photo"] = profile.photo

    return user_data


@login_required(login_url='/accounts/login')
def index(request):
    user_data = get_data(request)
    return render(request, 'settings/settings.html', user_data)


@login_required(login_url='/accounts/login')
def save(request):
    user_data = get_data(request)

    if request.method == 'POST':
        photo = request.FILES.get("profile_image")
        first_name = request.POST.get("settings_first_name")
        last_name = request.POST.get("settings_last_name")
        email = request.POST.get("settings_email")
        phone_number = request.POST.get("settings_phone_number")
        birthdate = request.POST.get("settings_birthdate")
        password = request.POST.get("settings_password")

        if first_name:
            first_name = first_name.strip().title()
            if not first_name:
                messages.error(request, 'First Name is not valid')
                return redirect('settings')

        if last_name:
            last_name = last_name.strip().title()
            if not last_name:
                messages.error(request, 'Last Name is not valid')
                return redirect('settings')

        if email:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                messages.error(request, 'Email is not valid')
                return redirect('settings')

            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, 'Email is being used by another user')
                return redirect('settings')

        if password:
            try:
                validate_password(password)
            except Exception as e:
                messages.error(request, 'Password does not meet requirements')
                return redirect('settings')

        valid_phone_number = False
        if phone_number:
            try:
                if carrier._is_mobile(number_type(phonenumbers.parse(phone_number))) is True:
                    valid_phone_number = True
                else:
                    messages.error(request, 'Phone number is not valid')
                    return redirect('settings')
            except Exception as e:
                messages.error(request, 'Phone number is not valid')
                return redirect('settings')

        valid_photo = False
        if photo:
            fs = FileSystemStorage()
            filename = fs.save(
                os.path.join(settings.MEDIA_ROOT, "photos", "users", request.user.username + "_profile.png"), photo)
            try:
                trial_image = Image.open(filename)
                trial_image.verify()
                uploaded_file_url = fs.url(filename)
                valid_photo = True
            except Exception as e:
                try:
                    os.remove(filename)
                except Exception as e:
                    pass
                messages.error(request, 'Photo is not valid')
                return redirect('settings')

        user_update_dict = dict()
        profile_update_dict = dict()

        if first_name:
            user_data["user_first_name"] = first_name
            user_update_dict["first_name"] = first_name

        if last_name:
            user_data["user_last_name"] = last_name
            user_update_dict["last_name"] = last_name

        if email:
            user_data["user_email"] = email
            user_update_dict["email"] = email

        if phone_number and valid_phone_number:
            user_data["user_phone_number"] = phone_number
            profile_update_dict["phone_number"] = phone_number

        if birthdate:
            birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
            user_data["user_birthdate"] = "{}/{}/{}".format(birthdate.month, birthdate.day, birthdate.year)
            profile_update_dict["birthdate"] = make_aware(birthdate)

        if photo and valid_photo:  # create
            user_data["user_photo"] = uploaded_file_url
            profile_update_dict["photo"] = uploaded_file_url

        if password:
            user = User.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()

        User.objects.filter(id=request.user.id).update(**user_update_dict)
        Profile.objects.filter(user_id=request.user.id).update(**profile_update_dict)

        messages.success(request, 'Your data has been changed')
        return render(request, 'settings/settings.html', user_data)
    else:
        return render(request, 'settings/settings.html', user_data)
