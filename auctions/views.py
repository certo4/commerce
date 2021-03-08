from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, ListingForm
from .forms import CloseListing, WatchlistAction


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "is_index": True,
        "is_watchlist": False
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

@login_required
def create_listing(request):

    form = ListingForm(request.POST)
    # Check whether form is valid:
    if form.is_valid():

        # Create new listing
        l = Listing(
            title = form.cleaned_data["title"],
            # seller = current_user,
            description = form.cleaned_data["description"],
            starting_bid = form.cleaned_data["starting_bid"],
            img_url = form.cleaned_data["img_url"],
            seller_username = request.user.username,
            category_id = form.cleaned_data["category_id"],
            current_price = 0,
            is_active = True,
            # current_winner = current_user
        )
        l.save()
        l.seller.add(request.user)
        l.current_winner.add(request.user)
        #l.category_id.set()
        

        return render(request, "auctions/test.html", {
            "listing": l
        })
    else:
        return HttpResponseRedirect(reverse("new_listing"))

def listing(request, id):
    # Getting the object
    listing = Listing.objects.get(id=id)
    if request.user.is_authenticated:

        # Setting watchlist form button text
        watchlist_text = "Add to Watchlist"
        watchlist_form = WatchlistAction(initial={'set_watchlist':True})
        if listing.in_watchlist:
            watchlist_text = "Remove from Watchlist"
            watchlist_form = WatchlistAction(initial={'set_watchlist':False})

        #Checking whether current user is the owner of listing
        # is_owner = False
        # if listing.seller_username == request.user.username:
        #     is_owner = True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_authenticated": request.user.is_authenticated,
            "watchlist_form": watchlist_form,
            "watchlist_text": watchlist_text
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_authenticated": request.user.is_authenticated,
            "watchlist_form": False,
            "watchlist_text": ""
        })

@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(
            in_watchlist=True, 
            seller_username=request.user.username
        ),
        "is_index": False,
        "is_watchlist": True
    })

def watchlist_action(request, id):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request:
        form = WatchlistAction(request.POST)
        # Check whether it's valid:
        if form.is_valid():
            # Get listing object and new in_watchlist value
            listing = Listing.objects.get(id=id)
            set_watchlist = bool(form.cleaned_data["set_watchlist"])

            # Set the new value for in_watchlist
            if set_watchlist:
                listing.in_watchlist = True
                listing.save()
            else:
                listing.in_watchlist = False
                listing.save()

            return render(request, "auctions/test.html", {
                "listing": listing,
                "add_watchlist": set_watchlist,
                # "form_info": form_info,
                # "form_info_type": form_info_type,
                # "add_watchlist_type": request.POST
            })

    # If a GET (or any other method) we'll create a blank form
    else:
        form = WatchlistAction()
    
    return HttpResponseRedirect(f'/listings/{id}')
