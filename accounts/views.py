from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "این شماره تلفن قبلاً ثبت شده است.")
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        user = User.objects.create_user(
            username=username,
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='customer'
        )
        login(request, user, backend='accounts.backends.PhoneOrUsernameBackend')
        messages.success(request, "ثبت‌نام شما با موفقیت انجام شد.")
        return redirect('home')

    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=identifier, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"خوش آمدید، {user.first_name or user.username}")
        else:
            messages.error(request, "نام کاربری/شماره تلفن یا رمز عبور اشتباه است.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

def logout_view(request):
    logout(request)
    messages.info(request, "با موفقیت از حساب کاربری خارج شدید.")
    return redirect('home')

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()

        new_password = request.POST.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)
            user.save()
            login(request, user, backend='accounts.backends.PhoneOrUsernameBackend')
        else:
            user.save()

        messages.success(request, "اطلاعات پروفایل با موفقیت بروزرسانی شد.")

    return redirect(request.META.get('HTTP_REFERER', 'home'))