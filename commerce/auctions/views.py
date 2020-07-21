import sqlite3, datetime, os, os.path

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse,include, path
from django.contrib import admin
from django import forms

from . import views

from .models import User, Listings, Categories, Bids, Comments, Watchlist



def index(request):
    d = datetime.datetime.now()
    context={
            "d" : d,
            "ActiveListings": Listings.objects.all(),
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")



"""               NEW
   -----------------------------------------------------------------------------------
"""

#Create Listing

def CreateListings_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":
        Ltitle=request.POST["Ltitle"]
        Ccode= int(request.POST["Ccode"])
        Ldescription=request.POST["Ldescription"]
        Lprice=float(request.POST["Lprice"].replace(',', '.'))
        Ldatestart=request.POST["Ldatestart"]
        Lduration=request.POST["Lduration"]
        Luser=request.POST["Luser"]
        Lstatus=request.POST["Lstatus"]
        Limage="media/"+str(request.POST["Limage"])
        #Lastid = Listings.objects.latest('id')

        try:
            Listings_create = Listings.objects.create(Ltitle=Ltitle, Ccode=Ccode, Ldescription=Ldescription, Lprice= Lprice, Ldatestart=Ldatestart, Lduration=Lduration, Luser=Luser, Limage=Limage, Lstatus=Lstatus )
            Listings_create.save()

        except IntegrityError:
            context={
                "message": "Title already exists, please choose other Title",
                "d" : d ,
                "Categories": Categories.objects.all(),
            }
            return render(request, "auctions/CreateListings.html", context)

        context={
                "d" : d,
                "ActiveListings": Listings.objects.all(),
        }
        return render(request, "auctions/index.html", context)

    else:
        context={
            "d" : d ,
            "Categories": Categories.objects.all(),
        }
        return render(request, "auctions/CreateListings.html", context)


"""
Watchlist: Users who are signed in should be able to visit a Watchlist page, which
should display all of the listings that a user has added to their watchlist.
Clicking on any of those listings should take the user to that listing’s page.
"""

def Watchlist_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":





        context={
          "d" : d,
          "Watchlists" : Watchlist.objects.all(),
        }
        return render(request, "auctions/Listingspage.html", context)



    else:
        context={
           "d" : d,
           "Watchlists": Watchlist.objects.all(),
        }
        return render(request, "auctions/Watchlist.html", context)






"""
Categories: Users should be able to visit a page that displays a list of all
listing categories.
Clicking on the name of any category should take the user to a page that displays
all of the active listings in that category.
"""

#List Categories- drop down list?
def Categories_view(request):
    d = datetime.datetime.now()

    context= {
        "d": d,
        "Categories": Categories.objects.all(),
        }
    return render(request, "auctions/Categories.html", context)

#resolver problema

def CategoryShow_view(request, C_description):
    d = datetime.datetime.now()
    cat_filter=[]
    cat_data =[]
    cat_description=C_description
    print(f"PROCURAR",cat_description)
    try:
        cat_filter = Categories.objects.filter(Cdescription=cat_description)
        print(f"CODIGO: ",cat_filter)

        cat_code=cat_filter[0].Ccode
        print(f"cat_code: ",cat_code)


        cat_data = Listings.objects.filter(Ccode=cat_code)
        print(f"DADOS : ",cat_data)
        context= {
           "d" :d,
           "C_description" :cat_description ,
           "C_data" :cat_data,
        }
        return render(request, "auctions/CategoryShow.html", context)
    except:
        context= {
            "d" :d,
            "C_description" :cat_description ,
            "message":"Nothing to show in category:  " + C_description,
        }
        return render(request, "auctions/CategoryShow.html", context)




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
def Listingspage_view(request):
        d = datetime.datetime.now()
        context={
                "Listings": Listings.objects.all(),
                "d": d,
        }
        return render(request,"auctions/Listingspage.html", context)



def Bids_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":
        return HttpResponse("bids POST")

    else:
        return render(request, "auctions/Listingspage.html")


def  Comments_view(request):
    if request.method == "POST":
        return HttpResponse(" Comments POST")

    else:
        return render(request, "auctions/Listingspage.html")
