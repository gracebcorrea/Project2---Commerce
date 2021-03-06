# Generated by Django 3.0.8 on 2020-07-23 20:18

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
            model_name='listings',
            name='Limage',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='Lstatus',
            field=models.CharField(choices=[('Active', 'Active - Receiving Bids'), ('To Begin', 'To Begin - De Auction didn´t start yet'), ('Closed', 'Closed - The seller gave up the auction'), ('Sold', 'Sold')], max_length=8),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='Lcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listings'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cdate', models.DateField(blank=True, help_text='Please use the following format: <em>YYYY-MM-DD</em>. for the auction start')),
                ('Cuser', models.CharField(max_length=25)),
                ('Ccomment', models.CharField(max_length=250)),
                ('Lcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listings')),
            ],
        ),
    ]
