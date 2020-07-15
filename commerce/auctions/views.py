import sqlite3, datetime

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import admin


from .models import User


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


"""               NEW
   -----------------------------------------------------------------------------------
"""

"""
Create Listing: Users should be able to visit a page to create a new listing.
They should be able to specify a title for the listing, a text-based description,
and what the starting bid should be. Users should also optionally be able to provide
a URL for an image for the listing and/or a category
(e.g. Fashion, Toys, Electronics, Home, etc.).
"""

#Create Listing
def CreateListings(request):
    if request.method == "POST":
        return HttpResponse("Create listings POST")

    else:
        return render(request, "auctions/createlistings.html")

"""
Categories: Users should be able to visit a page that displays a list of all
listing categories.
Clicking on the name of any category should take the user to a page that displays
all of the active listings in that category.
"""

#List Categories- drop down list?
def Categories(request):
    if request.method == "POST":
        return HttpResponse("Categories POST")

    else:
        return render(request, "auctions/Categories.html")

"""
Listing Page: Clicking on a listing should take users to a page specific to that listing.
On that page, users should be able to view all details about the listing, including the
current price for the listing.
If the user is signed in, the user should be able to add the item to their “Watchlist.”
If the item is already on the watchlist, the user should be able to remove it.
If the user is signed in, the user should be able to bid on the item.
The bid must be at least as large as the starting bid, and must be greater than any
other bids that have been placed (if any). If the bid doesn’t meet those criteria,
the user should be presented with an error.
If the user is signed in and is the one who created the listing, the user should have
the ability to “close” the auction from this page, which makes the highest bidder
the winner of the auction and makes the listing no longer active.
If a user is signed in on a closed listing page, and the user has won that auction,
the page should say so.
Users who are signed in should be able to add comments to the listing page.
The listing page should display all comments that have been made on the listing.
"""
#List Listings details -  All
def Listings(request):
    if request.method == "POST":
        return HttpResponse("listings POST")

    else:
        return render(request, "auctions/listings.html")




"""
Active Listings Page: The default route of your web application should let users
view all of the currently active auction listings. For each active listing, this
page should display (at minimum) the title, description, current price, and photo
 (if one exists for the listing).
"""
def ActiveListings(request):
    if request.method == "POST":
        return HttpResponse("ActiveListings POST")

    else:
        return render(request, "auctions/index.html")


def Bids(request):
    if request.method == "POST":
        return HttpResponse("bids POST")

    else:
        return render(request, "auctions/bids.html")

"""
Watchlist: Users who are signed in should be able to visit a Watchlist page, which
should display all of the listings that a user has added to their watchlist.
Clicking on any of those listings should take the user to that listing’s page.
"""

def Watchlist(request):
    if request.method == "POST":
        return HttpResponse("Watchlist POST")

    else:
        return render(request, "auctions/Watchlist.html")



def  Comments(request):
    if request.method == "POST":
        return HttpResponse(" Comments POST")

    else:
        return render(request, "auctions/comments.html")

def SoldTo(request):
    if request.method == "POST":
        return HttpResponse("soldto POST")

    else:
        return render(request, "auctions/soldto.html")
