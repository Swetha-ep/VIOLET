# Generated by Django 4.2.1 on 2023-07-01 13:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_banner'),
        ('cart', '0017_alter_profile_phone_alter_profile_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
        migrations.AlterField(
            model_name='cartt',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
