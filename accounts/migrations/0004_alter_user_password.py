# Generated by Django 5.1.5 on 2025-01-21 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_staff_user_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
