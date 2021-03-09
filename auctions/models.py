from django.contrib.auth.models import AbstractUser
from django.db import models

from django.forms import ModelForm

CATEGORIES = [
    ('furniture', 'Furniture'),
    ('electronics', 'Electronics'),
    ('art', 'Art'),
    ('other', 'Other')
]

class User(AbstractUser):
    def __str__(self):
        return self.username
    pass

class Category(models.Model):
    pass

class Listing(models.Model):

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    seller = models.ManyToManyField(User, blank=True, related_name="listing")
    seller_username = models.CharField(max_length=64, default="")
    img_url = models.CharField(max_length=64, blank=True) 
    category = models.CharField(max_length=64, choices=CATEGORIES, default="art")
    in_watchlist = models.BooleanField(default=False)
    current_price = models.IntegerField(blank=True) 
    is_active = models.BooleanField()
    current_winner = models.ManyToManyField(User, blank=True, related_name="won_bid")
    current_winner_username = models.CharField(max_length=64, blank=True, default="")

    def __str__(self):
        return self.title

    # TODO: Make a helper function that will check if current user is owner

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'img_url', 'category']
