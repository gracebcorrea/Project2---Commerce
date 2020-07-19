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


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


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


"""
Create Listing: Users should be able to visit a page to create a new listing.
They should be able to specify a title for the listing, a text-based description,
and what the starting bid should be. Users should also optionally be able to provide
a URL for an image for the listing and/or a category
(e.g. Fashion, Toys, Electronics, Home, etc.).
"""

#Create Listing
def CreateListings_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":
        Ltitle=request.POST["Ltitle"]
        Ccode=request.POST["Ccode"]
        Ldescription=request.POST["Ldescription"]
        Lprice=request.POST["Lprice"]
        Ldatestart=request.POST["Ldatestart"]
        Lduration=request.POST["Lduration"]
        Luser=request.POST["Luser"]
        Limage=request.POST["Limage"]
        Lstatus=request.POST["Lstatus"]
        print("Trying to SAVE   -> :" , [Ltitle],  [Ccode] , [Lprice] , [Ldatestart], [Ldescription])
        print("Details   -> :" , [Lduration]  ,  [Luser],[Limage] , [Lstatus] )

        fieldtranslate ={"Ltitle":Ltitle}
        if db.execute("SELECT * FROM auctions_listings WHERE Ltitle = :Ltitle " ,fieldtranslate):
            context: {
                 "CheckMessage" : "This title already exits please choose another Title",
                 "Date" : d ,
                 "Categories": Categories.objects.all(),
            }
            return render(request, "auctions/CreateListings.html", context)
        else:
            try:
                fieldtranslate ={"Ltitle":Ltitle,"Ccode":Ccode,"Ldescription": Ldescription,"Lprice":Lprice,"Ldatestart":Ldatestart,"Lduration":Lduration,"Luser":Luser,"Lstatus":Lstatus,"Limage": Limage}
                values = ":Ltitle,:Ccode, :Ldescription,:Lprice,:Ldatestart,:Lduration,:Luser,:Lstatus,:Limage"
                db.execute("INSERT INTO auctions_listings ( Ltitle,Ccode, Ldescription,Lprice,Ldatestart,Lduration,Luser,Lstatus,Limage) VALUES (values)",fieldtranslate)
                db.commit()
                return HttpResponseRedirect(reverse("auctions:index"))
            except (x) as error:
                context={
                  "message": "Error trying to insert new listing, please contact support",
                  "Date" : d ,
                  "Categories": Categories.objects.all(),
                }
                return render(request, "auctions/CreateListings.html" , context)

    else:
        context={
              "message": "Fields with * are required to save the listing"
              "Date" : d ,
              "Categories": Categories.objects.all(),
        }
        return render(request, "auctions/CreateListings.html", context)







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
        "Categories": Categories.objects.all(),
        }
    return render(request, "auctions/Categories.html", context)

#resolver problema
def CategoryShow_view(request, C_id, C_description):
    try:
       category_id = Categories.objects.get(id=C_id)
       category_description = Categories.objects.get(Cdescription=C_description)
       listings="working on this"
    except Categories.DoesNotExist:
        raise Http404("Categories does not exist")

    context= {
            "category_id" :category_id,
            "category_description" :category_description,
            "Listings": listings,
            "d" :d,
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
def Listings_view(request):
        d = datetime.datetime.now()
        context={
                "Listings": Listings.objects.all(),
                "d": d,
        }
        return render(request,"auctions/Listings.html", context)







def Bids_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":
        return HttpResponse("bids POST")

    else:
        return render(request, "auctions/Bids.html")


def  Comments_view(request):
    if request.method == "POST":
        return HttpResponse(" Comments POST")

    else:
        return render(request, "auctions/Comments.html")



"""
Watchlist: Users who are signed in should be able to visit a Watchlist page, which
should display all of the listings that a user has added to their watchlist.
Clicking on any of those listings should take the user to that listing’s page.
"""

def Watchlist_view(request):
    d = datetime.datetime.now()
    if request.method == "POST":


        context={
            "message" :"Entrei no Post",
            "Whatchlists" : Watchlist.objects.all(),
        }
        return render(request, "auctions/WatchList.html", context)
    else:
        context={
            "message":"Nao entrei no Post"
        }
        return render(request, "auctions/WatchList.html", context)



#https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})
