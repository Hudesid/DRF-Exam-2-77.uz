# Generated by Django 5.1.5 on 2025-01-21 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='announcement.category'),
        ),
    ]
