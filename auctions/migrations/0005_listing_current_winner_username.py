# Generated by Django 3.1.6 on 2021-03-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_in_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_winner_username',
            field=models.CharField(default='', max_length=64),
        ),
    ]
