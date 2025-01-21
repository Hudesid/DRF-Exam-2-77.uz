import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=8)
    product = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    phone_number = models.CharField(max_length=12, validators=[RegexValidator(
            regex=r'^\+9989\d{8}$',
            message="Phone number must start with '+9989' and be followed by 8 digits."
        )])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="user", null=True)
    is_active = models.BooleanField(default=False)

    object = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["username", "password"]

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def validate_address(self):
        return self.validate_address
