# Generated by Django 5.1.5 on 2025-01-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0002_alter_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
    ]
