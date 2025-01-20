import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from .managers import CustomUserManager, CategoryManager
from django.contrib.auth.models import AbstractBaseUser


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def ads_count(self):
        ads_count = self.products.count()
        for child in self.children.all():
            ads_count += child.ads_count()
        return ads_count

# class BaseModel(models.Model):
#     guid = models.UUIDField(
#         unique=True, default=uuid.uuid4, editable=False, db_index=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=8)
    product = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    phone_number = models.CharField(max_length=255, validators=[RegexValidator(
            regex=r'^\+9989\d{8}$',
            message="Phone number must start with '+9989' and be followed by 8 digits."
        )])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="user", null=True)


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


class AddressUser(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="validate_address")

    def __str__(self):
        return self.name


class Product(models.Model):
    currency_choice = [('UZS', 'UZS'), ('RUB', 'RUB'), ('USD', 'USD')]
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    phone_number = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    author = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, choices=currency_choice, default=currency_choice[0])
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    seller = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def validate_address(self):
        return self.validate_address

    def get_extra(self):
        if self.extra.__str__() == 'Status: active':
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(models.Model):
    district = models.ForeignKey(District, related_name='addresses', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    user = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='validate_address')

    def __str__(self):
        return self.name


class Extra(models.Model):
    is_mine = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    expires_at = models.DateTimeField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='extra')

    def __str__(self):
        return f"Status: {self.status}"


class PrivacyPolicy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

