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



#Create Listing
def CreateListings(request):
    if request.method == "POST":
        return HttpResponse("Create listings POST")

    else:
        return render(request, "auctions/createlistings.html")

#List Listings details -  All
def Listings(request):
    if request.method == "POST":
        return HttpResponse("listings POST")

    else:
        return render(request, "auctions/Listings.html")


#List Categories
def Categories(request):
    if request.method == "POST":
        return HttpResponse("Categories POST")

    else:
        return render(request, "auctions/Categories.html")



def ActiveListings(request):
    if request.method == "POST":
        return HttpResponse("property POST")

    else:
        return render(request, "auctions/ActiveListings.html")


def Bids(request):
    if request.method == "POST":
        return HttpResponse("bids POST")

    else:
        return render(request, "auctions/bids.html")
def Watchlist(request):
    if request.method == "POST":
        return HttpResponse("Watchlist POST")

    else:
        return render(request, "auctions/Watchlist.html")



def  Comments(request):
    if request.method == "POST":
        return HttpResponse(" Comments POST")

    else:
        return render(request, "auctions/Comments.html")

def SoldTo(request):
    if request.method == "POST":
        return HttpResponse("soldto POST")

    else:
        return render(request, "auctions/soldto.html")
