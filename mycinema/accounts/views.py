from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        # Register User
        return
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        # Login User
        return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    return redirect('login')


def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
