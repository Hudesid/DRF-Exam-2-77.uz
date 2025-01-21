from django.contrib.auth.models import BaseUserManager
from django.db import models
from rest_framework.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The Full name must be")
        if not password:
            raise ValueError("The Password must be")
        username = username.lower()
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CategoryManager(models.Manager):
    def get_root_categories(self):
        return self.filter(parent__isnull=True)

    def children(self, id):
        try:
            parent = self.get(guid=id)
        except self.model.DoesNotExist:
            raise ValidationError(
                {"product": f"Object with guid={id} does not exist."},
                code="DOES_NOT_EXIST",
            )
        return parent.child.all()

    def _build_tree(self, parent=None):
        categories = self.all()
        tree = []
        children = categories.filter(parent=parent)
        for child in children:
            sub_tree = self._build_tree(categories, parent=child)
            tree.append({
                'category': child,
                'children': sub_tree
            })
        return tree