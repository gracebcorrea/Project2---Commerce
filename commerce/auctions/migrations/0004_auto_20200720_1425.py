# Generated by Django 3.0.8 on 2020-07-20 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200717_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='Limage',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
