from django.contrib import admin
from . import models


class ImageInLine(admin.TabularInline):
    model = models.Image
    extra = 1
    raw_id_fields = ('product',)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at', 'product')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'product', 'category')


@admin.register(models.AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'long', 'user')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'currency', 'seller')
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [ImageInLine]


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'long', 'user', 'district')


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'addresses')


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'districts')


@admin.register(models.Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_mine', 'status', 'expires_at', 'product')


@admin.register(models.PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')