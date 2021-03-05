from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, ListingForm


def index(request):
    return render(request, "auctions/index.html")


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
    # Getting current user object
    current_user = request.user

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
