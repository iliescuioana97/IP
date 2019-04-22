from django.shortcuts import render, redirect


def register(request):
    # if request.method == 'POST':
    #     print('SUBMITTED REG')
    #     return redirect('login')
    # else:
    #     return render(request, 'accounts/register.html')
    return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return redirect('login')


def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
