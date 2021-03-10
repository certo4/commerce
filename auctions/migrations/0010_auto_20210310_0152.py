# Generated by Django 3.1.6 on 2021-03-10 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210309_0427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(blank=True, max_length=100)),
                ('listing_id', models.IntegerField(blank=True, default=0, null=True)),
                ('commenter_username', models.CharField(blank=True, default='', max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='bid',
            name='bidder_user',
        ),
    ]
