# Generated by Django 5.1.5 on 2025-01-22 01:10

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_groups_user_user_permissions'),
        ('common', '0002_remove_addressuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='validate_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='common.addressuser'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must start with '+9989' and be followed by 8 digits.", regex='^\\+9989\\d{8}$')]),
        ),
    ]
