# Generated by Django 5.1.2 on 2024-10-15 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('propertyapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenant',
            old_name='document',
            new_name='image',
        ),
    ]
