from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('guid', 'is_staff', 'is_active', 'username', 'phone_number', 'product', 'category')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'phone_number')
    ordering = ('username',)
    readonly_fields = ('last_login', 'date_joined', 'guid')
    fieldsets = (
        ('Personal Info', {
            'fields': ('guid', 'username', 'phone_number', 'profile_photo', 'address', 'validate_address')
        }),
        ('Seller Info', {
            'fields': ('category',),
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'role'),
        }),
        ('Change Password', {
            'fields': ('password',),
            'classes': ('collapse',),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )



admin.site.register(User, CustomUserAdmin)