from django.contrib.auth.models import AbstractUser
from django.db import models

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

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    seller = models.ManyToManyField(User, blank=True, related_name="listing")
    seller_username = models.CharField(max_length=64, default="")
    img_url = models.CharField(max_length=64, blank=True) 
    category = models.CharField(max_length=64, choices=CATEGORIES, default="art")
    in_watchlist = models.BooleanField(default=False)
    #TODO: Check for only positives and change default from 0!
    current_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    is_active = models.BooleanField()
    current_winner = models.ManyToManyField(User, blank=True, related_name="won_bid")
    current_winner_username = models.CharField(max_length=64, blank=True, default="")

    def __str__(self):
        return self.title

    # TODO: Make a helper function that will check if current user is owner

class Bid(models.Model):
    bid = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    bidder_username = models.CharField(max_length=64, blank=True, default="")
    # bidder_user = models.ManyToManyField(User, blank=True, related_name="bidder")



