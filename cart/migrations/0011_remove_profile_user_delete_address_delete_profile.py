# Generated by Django 4.2.1 on 2023-06-28 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_remove_profile_address_remove_profile_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
