import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, null=True)
    product = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    validate_address = models.ForeignKey("common.AddressUser", on_delete=models.SET_NULL, related_name="users", null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(
            regex=r'^\+9989\d{8}$',
            message="Phone number must start with '+9989' and be followed by 8 digits."
        )])
    category = models.ForeignKey("announcement.Category", on_delete=models.SET_NULL, related_name="user", null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)



