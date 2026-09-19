from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


def normalize_phone_number(phone_number):
    """
    Normalizes Nigerian phone numbers to E.164 format (+234...).
    Accepts 0801..., 234801..., or +234801... and returns +234801...
    """
    phone_number = phone_number.strip().replace(" ", "")
    if phone_number.startswith("0"):
        return "+234" + phone_number[1:]
    if phone_number.startswith("234"):
        return "+" + phone_number
    if phone_number.startswith("+234"):
        return phone_number
    return phone_number  # unrecognized format, left as-is for now


class UserManager(BaseUserManager):
    """
    Custom manager for our phone-based User model.
    Django's default manager assumes a username field; we override
    create_user / create_superuser to key off phone number instead.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        extra_fields.setdefault("role", User.Role.STUDENT)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model built on AbstractBaseUser (not Django's default
    User). Phone number is the login identifier — email is optional,
    used only if we need it for notifications later.
    """

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        ADMIN = "admin", "Admin"
        VENDOR = "vendor", "Vendor"  # for later: router/tool sellers, landlords, etc.

    phone_number = models.CharField(max_length=17, unique=True)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    is_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []  # phone_number + password are the only prompts on createsuperuser

    def save(self, *args, **kwargs):
        self.phone_number = normalize_phone_number(self.phone_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.phone_number
