# Generated by Django 3.1.6 on 2021-03-08 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210308_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category_id',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('furniture', 'Furniture'), ('electronics', 'Electronics'), ('art', 'Art'), ('other', 'Other')], default='art', max_length=64),
        ),
    ]
