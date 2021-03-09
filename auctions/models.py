from django.contrib.auth.models import AbstractUser
from django.db import models

from django.forms import ModelForm
from django import forms

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
    current_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
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

class Bid(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    bidder_username = models.CharField(max_length=64, blank=True, default="")
    bidder_user = models.ManyToManyField(User, blank=True, related_name="bidder")

class BiddingForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price', 'bidder_username']
        widgets = {'bidder_username': forms.HiddenInput()}

