# Generated by Django 3.0.8 on 2020-07-17 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bids_categories_comments_listings_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='Lcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listings'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='Lcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listings'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='Lcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listings'),
        ),
    ]
