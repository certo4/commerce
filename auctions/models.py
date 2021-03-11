from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Categories list of tuples for the the category field
CATEGORIES = [
    ('furniture', 'Furniture'),
    ('electronics', 'Electronics'),
    ('art', 'Art'),
    ('other', 'Other'),
    ('', '')
]


# Model for a user in the app
class User(AbstractUser):
    def __str__(self):
        return self.username
    pass


# Model of a listing object. Contains the required title,
# description, and starting bid as well as the optional
# category and image URL. Beyond those, I am using
# Many to many fields to create relationships between
# the models even if they are not used in the app.
class Listing(models.Model):
    title = models.CharField(max_length=64, default="")
    description = models.CharField(max_length=64, default="")
    starting_bid = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0.01,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    seller = models.ManyToManyField(User, blank=True, related_name="listing")
    seller_username = models.CharField(max_length=64, default="")
    img_url = models.CharField(max_length=64, blank=True, default="")
    category = models.CharField(
        max_length=64,
        choices=CATEGORIES,
        default="",
        blank=True
    )
    in_watchlist = models.BooleanField(default=False)
    watchlist_username = models.CharField(max_length=64, default="", blank=True)
    current_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        default=0
    )
    is_active = models.BooleanField(default=True)
    current_winner = models.ManyToManyField(
        User,
        blank=True,
        related_name="won_bid"
    )
    current_winner_username = models.CharField(
        max_length=64,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"{self.title} by {self.seller_username}"

    # Helper function to check if the submitted user is the seller
    def is_owner(self, submitted_username):
        if submitted_username == self.seller_username:
            return True
        return False

    # Helper function to check if the submitted user is the winner
    def is_winner(self, submitted_username):
        if submitted_username == self.current_winner_username:
            return True
        return False

    def new_bidders(self):
        if self.current_winner_username != self.seller_username:
            return True
        return False


# Model to represent a bid that will include the value of the bid
# itself, the bidder username and the listing.
class Bid(models.Model):
    bid = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    bidder_username = models.CharField(max_length=64, blank=True, default="")
    listing_id = models.ManyToManyField(
        Listing,
        blank=True,
        related_name="bid_on"
    )

    def __str__(self):
        return f"Bid of {self.bid} by {self.bidder_username} on listing {self.listing_id}"


# Model to represent a comment that will include the comment text,
# listing and the commenter username.
class Comment(models.Model):
    comment_text = models.CharField(max_length=100, blank=True)
    listing_id = models.ManyToManyField(
        Listing,
        blank=True,
        related_name="commented_on"
    )
    commenter_username = models.CharField(
        max_length=64,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"Comment by {self.commenter_username} on listing {self.listing_id}"
