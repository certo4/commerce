from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import User, Listing, CATEGORIES, Bid, Comment
from .forms import CloseListing, WatchlistAction, ListingForm, BiddingForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "is_watchlist": False,
        "is_category": False
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form,
        "message": ""
    })


# Function that will parse the information from the 
# Create Listing form and save it to database as well
# as redirect to the newly created listing.
@login_required
def create_listing(request):

    form = ListingForm(request.POST)
    # Check whether form is valid:
    if form.is_valid():

        # Create new listing
        listing = Listing(
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            starting_bid=form.cleaned_data["starting_bid"],
            img_url=form.cleaned_data["img_url"],
            seller_username=request.user.username,
            category=form.cleaned_data["category"],
            current_price=0,
            is_active=True,
        )
        listing.save()
        listing.seller.add(request.user)
        listing.current_winner.add(request.user)
        listing.save()

        #Redirect to newly created listing
        return HttpResponseRedirect(f'/listings/{listing.id}')

    else:

        # Redirect to create a new listing form
        return HttpResponseRedirect(reverse("new_listing"))


# Helper function to check if the current user is the winner and 
# return the current username otherwise return false
def get_winner(request, listing):
    is_winner = listing.is_winner(request.user.username)
    new_bidders = listing.new_bidders()

    if not listing.is_active and is_winner and new_bidders:
        return listing.current_winner_username
    return False


# Helper function to check if the listing is active
# and the owner viewing the form is the owner
def get_close_listing_form(request, listing):
    is_owner = listing.is_owner(request.user.username)
    if listing.is_active and is_owner:
        return CloseListing()
    return False


# View that will render each listing with all of its forms
# like make a bid, comment, watchlist and close the bid 
# forms if the user viewing the listing is the owner.
def listing(request, id):
    # Getting the object
    listing = Listing.objects.get(id=id)
    if request.user.is_authenticated:

        # Setting watchlist form button text
        watchlist_text = "Add to Watchlist"
        watchlist_form = WatchlistAction(initial={'set_watchlist': True})
        if listing.in_watchlist:
            watchlist_text = "Remove from Watchlist"
            watchlist_form = WatchlistAction(initial={'set_watchlist': False})


        # If necessary, populate the current_winner and close listing form
        current_winner = get_winner(request, listing)       
        close_listing_form = get_close_listing_form(request, listing)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_authenticated": request.user.is_authenticated,
            "watchlist_form": watchlist_form,
            "watchlist_text": watchlist_text,
            "close_listing_form": close_listing_form,
            "current_winner": current_winner,
            "bidding_form": BiddingForm(),
            "comment_form": CommentForm(),
            "comments": Comment.objects.filter(listing_id=id),
            "is_owner": listing.is_owner(request.user.username)
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_authenticated": request.user.is_authenticated,
            "watchlist_form": False,
            "watchlist_text": "",
            "comments": Comment.objects.filter(listing_id=id)
        })


# Function that renders all of the user's watchlisted items
@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(
            in_watchlist=True,
            watchlist_username=request.user.username
        ),
        "is_watchlist": True,
        "is_category": False
    })


# Function that will add an item to a user's watchlist
@login_required
def watchlist_action(request, id):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = WatchlistAction(request.POST)
        # Check whether it's valid:
        if form.is_valid():
            # Get listing object and new in_watchlist value
            listing = Listing.objects.get(id=id)
            listing.in_watchlist = bool(form.cleaned_data["set_watchlist"])
            listing.watchlist_username = request.user.username
            listing.save()

            return render(request, "auctions/test.html", {
                "listing": listing,
                "add_watchlist": listing.in_watchlist,
            })

    return HttpResponseRedirect(f'/listings/{id}')


# Function that will close an existing listing
@login_required
def close_listing(request, id):
    listing = Listing.objects.get(id=id)
    if request.user.username == listing.seller_username:
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(f'/listings/{id}')


# Function that passes all categories to the main
# category listing page
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })


# Function that will display all listings per category
def category(request, id):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(
            is_active=True,
            category=id
        ),
        "is_watchlist": False,
        "is_category": id
    })


@login_required
def bid(request, id):
    listing = Listing.objects.get(id=id)
    # If this is a POST request we need to process the form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = BiddingForm(request.POST)
        # Check whether it's valid:
        if form.is_valid():
            # Checking that the bid is higher than current price
            listing = Listing.objects.get(id=id)
            submitted_bid = Decimal(form.cleaned_data["bid"])
            acceptable_bid = is_acceptable_bid(submitted_bid, listing)

            # Create Bid if the bid is acceptable
            if acceptable_bid:
                b = Bid(
                    bid=submitted_bid,
                    bidder_username=request.user.username
                )
                b.save()
                b.listing_id.add(Listing.objects.get(pk=int(id)))
                b.save()

                # Save new price in listing object
                listing.current_price = submitted_bid
                listing.current_winner_username = request.user.username
                listing.save()
                listing.current_winner.add(request.user)
                listing.save()

                message = "Your bid was accepted. You are on the lead!"
            else:
                message = "Your bid is lower than or equal to the current bid. Big higher!"

            return render(request, "auctions/test.html", {
                "message": message,
            })

    return HttpResponseRedirect(f'/listings/{id}')


# Helper function to check whether a bid is acceptable
def is_acceptable_bid(submitted_bid, listing):
    # Checking that submitted bid is equal to or greater than starting bid
    # The default value of current price is zero and that is why
    # I am checking for that - to make sure that I am looking at the
    # first bid.
    if listing.current_price == 0:
        if submitted_bid >= listing.starting_bid:
            return True
    # Checking that submitted bid is greater than current price
    elif submitted_bid > listing.current_price:
        return True
    # Else the bid is not acceptable
    return False


def comment(request, id):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # Check whether it's valid:
        if form.is_valid():

            # Create comment
            c = Comment(
                comment_text=form.cleaned_data["comment_text"],
                commenter_username=request.user.username
            )
            c.save()
            c.listing_id.add(Listing.objects.get(pk=int(id)))
            c.save()

            return HttpResponseRedirect(f'/listings/{id}')

    # If a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return HttpResponseRedirect(f'/listings/{id}')
