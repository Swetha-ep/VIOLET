# Generated by Django 4.2.1 on 2023-07-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_offer_product_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
