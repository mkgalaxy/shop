from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('نام کاربری باید وارد شود')
        if not phone_number:
            raise ValueError('شماره تلفن باید وارد شود')
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number="09000000000", password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(username, phone_number, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'مشتری'),
        ('admin', 'مدیر'),
    )

    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name="نقش کاربر")

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"