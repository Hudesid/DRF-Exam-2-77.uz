# Generated by Django 5.1.5 on 2025-01-29 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_id_user_guid_user_role_alter_user_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
    ]
