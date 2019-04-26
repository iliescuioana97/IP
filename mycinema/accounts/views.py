from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

import re


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        terms = request.POST.get('terms')

        # Check agreement
        if not terms or terms != "1":
            messages.error(request, 'You must accept the terms and conditions')
            return redirect('register')

        # Check username
        username = username.strip().lower()
        if not username:
            messages.error(request, 'Username is not valid')
            return redirect('register')

        # Check first_name, last_name
        if first_name:
            first_name = first_name.strip().title()
            if not first_name:
                messages.error(request, 'First Name is not valid')
                return redirect('register')
        if last_name:
            last_name = last_name.strip().title()
            if not last_name:
                messages.error(request, 'Last Name is not valid')
                return redirect('register')

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is being used by another user')
                    return redirect('register')
                else:
                    # Check valid mail
                    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                        messages.error(request, 'Email is not valid')
                        return redirect('register')

                    try:
                        validate_password(password)
                    except Exception as e:
                        messages.error(request, 'Password does not meet requirements')
                        return redirect('register')

                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'accounts/forgot_password.html')
