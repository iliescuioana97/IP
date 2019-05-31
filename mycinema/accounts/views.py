from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

import re


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    # Function to make code cleaner and more readable
    def redirect_register():

        # Set the new values for cookies
        cookie_fname = request.POST['first_name']
        cookie_lname = request.POST['last_name']
        cookie_email = request.POST['email']
        cookie_username = request.POST['username']

        response = redirect('register')

        # max_age - 60 seconds availability, cookies reset
        # Assuming that the user doesn't need more than 60 seconds to make an account
        max_age_seconds = 60
        response.set_cookie('cookie_fname', cookie_fname, max_age=max_age_seconds)
        response.set_cookie('cookie_lname', cookie_lname, max_age=max_age_seconds)
        response.set_cookie('cookie_email', cookie_email, max_age=max_age_seconds)
        response.set_cookie('cookie_username', cookie_username, max_age=max_age_seconds)

        return response

    # Default values for cookies
    cookie_fname, cookie_lname, cookie_email, cookie_username = '', '', '', ''

    # If the cookies are already set, just grab them to render
    if {'cookie_username', 'cookie_email', 'cookie_fname', 'cookie_lname'} & request.COOKIES.keys():
        cookie_username = request.COOKIES['cookie_username']
        cookie_fname = request.COOKIES['cookie_fname']
        cookie_lname = request.COOKIES['cookie_lname']
        cookie_email = request.COOKIES['cookie_email']

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
            return redirect_register()

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
                        return redirect_register()

                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)

                    # is_active = False until he confirms his email
                    user.is_active = False
                    user.save()
                    messages.success(request, 'We\'ve sent you a confirmation email, in order to complete the registration')

                    # Sending email confirmation stuff
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your MyCinema account'
                    message = render_to_string('registration/account_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }, request=request)

                    email_object = EmailMessage(mail_subject, message, to=[email])
                    email_object.send()

                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        response = render(request, 'accounts/register.html', context={
            'cookie_username': cookie_username,
            'cookie_fname': cookie_fname,
            'cookie_lname': cookie_lname,
            'cookie_email': cookie_email})

        return response


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    login_username = ''
    if 'login_username' in request.COOKIES:
        login_username = request.COOKIES['login_username']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # if user has confirmed email
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')

                # Setting the cookie for username
                response = redirect('index')
                response.set_cookie('login_username', username)

                return response

            else:
                messages.error(request, 'User has not confirmed his email')
                login_username = request.POST['username']

                response = redirect('login')
                response.set_cookie('login_username', login_username)
                return response

        else:
            messages.error(request, 'Invalid credentials')
            login_username = request.POST['username']

            response = redirect('login')
            response.set_cookie('login_username', login_username)

            return response

    else:
        return render(request, 'accounts/login.html', context={'login_username': login_username})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist as e:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')

    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('login')
