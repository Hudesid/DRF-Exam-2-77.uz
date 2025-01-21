import uuid
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from .managers import CategoryManager
from accounts.models import User


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


class Extra(models.Model):
    is_mine = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='not active')
    expires_at = models.DateTimeField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='extra')

    def __str__(self):
        return f"Status: {self.status}"

    @property
    def current_status(self):
        if self.expires_at <= timezone.now() and self.status == 'active':
            self.status = 'not active'
            self.save()
        return self.status


class PopularSearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True)
    count = models.IntegerField()

    def __str__(self):
        return self.word

