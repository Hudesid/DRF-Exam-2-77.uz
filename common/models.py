from django.db import models
from django.utils.text import slugify
from announcement.models import Product
from accounts.models import User


class AddressUser(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    long = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="validate_address")

    def __str__(self):
        return self.name


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
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='validate_address')

    def __str__(self):
        return self.name


class StaticPage(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
