# Generated by Django 3.0.8 on 2020-07-17 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200716_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='picture',
            field=models.ImageField(blank=True, upload_to=b'images'),
        ),
    ]
