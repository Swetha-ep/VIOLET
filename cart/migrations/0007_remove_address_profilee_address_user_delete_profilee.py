# Generated by Django 4.2.1 on 2023-06-26 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0006_profilee_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='profilee',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Profilee',
        ),
    ]
