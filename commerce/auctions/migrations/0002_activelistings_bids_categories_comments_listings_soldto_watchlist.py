# Generated by Django 3.0.8 on 2020-07-16 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lcode', models.IntegerField()),
                ('Pcode', models.IntegerField()),
                ('dateStart', models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')),
                ('duration', models.IntegerField(help_text='Duration expressed in days')),
                ('status', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bcode', models.IntegerField()),
                ('Lcode', models.IntegerField()),
                ('Pcode', models.IntegerField()),
                ('user', models.CharField(max_length=25)),
                ('Bthrow', models.IntegerField()),
                ('Bprice', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ccode', models.IntegerField()),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ccode', models.IntegerField()),
                ('Lcode', models.IntegerField()),
                ('user', models.CharField(max_length=25)),
                ('comment', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pcode', models.IntegerField()),
                ('Ccode', models.IntegerField(help_text='Category House, Apartament, Commercial')),
                ('description', models.CharField(max_length=250)),
                ('picture', models.ImageField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, help_text='Just USD', max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='SoldTo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Scode', models.IntegerField()),
                ('Lcode', models.IntegerField()),
                ('Pcode', models.IntegerField()),
                ('user', models.CharField(max_length=25)),
                ('date', models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')),
                ('Bprice', models.DecimalField(decimal_places=2, max_digits=9)),
                ('status', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Wcode', models.IntegerField()),
                ('Lcode', models.IntegerField()),
                ('user', models.CharField(max_length=25)),
            ],
        ),
    ]
