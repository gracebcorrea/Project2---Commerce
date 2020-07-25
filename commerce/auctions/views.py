import sqlite3, datetime, os, os.path
import time
from datetime import datetime
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
    d = datetime.now()
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
    d = datetime.now()
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



def Watchlist_view(request):
    d = datetime.now()
    try:
        W = Watchlist.objects.all()
        context={
           "d" : d,
           "Wishlists": W,
        }
        return render(request, "auctions/Watchlist.html", context)
    except:
        context={
          "d" : d,
        }
        return render(request, "auctions/Watchlist.html", context)

def Watchlist_add(Lcode,user):
    W_Lcode=Lcode
    W_user=user
    try:
        Watchlist_create= Watchlist.objects.create(Lcode=W_Lcode,user=W_user,Wflag=1)
        Watchlist_create.save()
    except IntegrityError:
        return HttpResponse(" Integryty Error tryng to save new watchlist item")

    return None

def Watchlist_remove(Lcode,user):
    W_Lcode=Lcode
    W_user=user

    try:
        W_remove=Watchlist.objects.filter(Lcode=W_Lcode,user=W_user).delete()
        W_remove.save()

    except IntegrityError:
        return HttpResponse(" Integryty Error tryng to delete watchlist item")
    return None





def Categories_view(request):
    d = datetime.now()

    context= {
        "d": d,
        "Categories": Categories.objects.all(),
        }
    return render(request, "auctions/Categories.html", context)

#resolver problema

def CategoryShow_view(request, C_description):
    d = datetime.now()
    cat_filter=[]
    cat_data =[]
    cat_description=C_description

    try:
        cat_filter = Categories.objects.filter(Cdescription=cat_description)
        cat_code=cat_filter[0].Ccode
        cat_data = Listings.objects.filter(Ccode=cat_code)

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
    d = datetime.now()
    context={
       "d": d,
       "Listings": Listings.objects.all(),
       "Watchlist":Watchlist.objects.all(),
    }
    return render(request,"auctions/Listingspage.html", context)




def Bids_view(request, Btitle):
    B_title =Btitle
    d = datetime.now()
    L_data =[]
    W_data=[]
    B_data=[]
    C_data=[]
    #take data from desired listing
    L_data = Listings.objects.filter(Ltitle=B_title)
    #Take Watchlist
    W_data=Watchlist.objects.filter(Lcode__Ltitle=B_title)
    #take all bids for this listing
    B_data=Bids.objects.filter(Lcode__Ltitle=B_title)
    #Teke comments for this listing
    C_data=Comments.objects.filter(Lcode__Ltitle=B_title)

    if request.method == "POST":
        B_user = request.POST["B_Buser"]
        B_price =float(request.POST["B_Bprice"].replace(',', '.'))
        B_date = time.strftime("%Y-%m-%d")
        Lfilter = Listings.objects.filter(Ltitle=B_title).values('id' , 'Lprice')

        for Search_id in Lfilter:
            Lid_value = Search_id['id']
            Lprice = Search_id['Lprice']

        Lances= Bids.objects.filter(Lcode_id=Lid_value).values('Bthrow', 'Bprice').order_by('Bthrow')
        if len(Lances):
            for L in Lances:
               N_Bthrow = L['Bthrow']
               N_Bprice = L['Bprice']

            B_throw = N_Bthrow + 1
            print ("B_Bthrow IS:", B_Bthrow )
        else:
            B_throw = 1

        if B_price < Lprice:
            msgbids= "A new bid must be higher from the original price"

        if B_price <  N_Bprice :
            msgbids= "A new bid must be higher Than the highest Bid"


        try:
            print("I will try to save new BID")
            Bids_create = Bids.objects.create(Lcode=Lcode_id , Buser=B_user , Bthrow=B_throw, Bprice=B_price   ,Bdate=B_date )
            Bids_create.save()
            #get data with new bid to show on form
            B_data=Bids.objects.filter(Lcode__Ltitle=B_title)

            msgbids ="New Bid Saved"
            context={
            "msgbids":msgbids ,
            "d":d,
            "Btitle" : Btitle,
            "L_data" :L_data,
            "B_data" :B_data,
            "W_data" :W_data,
            "C_data":C_data,
             }
            return render(request, "auctions/BidsDetail.html", context)

        except:
            context={
                "msgbids": "Could not save Bid, please try agaiu",
                "d":d,
                "Btitle" : Btitle,
                "L_data" :L_data,
                "B_data" :B_data,
                "W_data" :W_data,
                "C_data":C_data,
            }
            return render(request, "auctions/BidsDetail.html", context)


    else:
        context = {
            "message" : "Not in BID POST",
            "d":d,
            "Btitle":B_title,
            "L_data":L_data,
            "B_data":B_data,
            "W_data":W_data,
            "C_data":C_data,
        }
        return render(request, "auctions/BidsDetail.html", context)





def  Comments_view(request):
    if request.method == "POST":

        return redirect(request.META["auctions/BidsDetail.html"])

    else:
        return redirect(request.META["auctions/BidsDetail.html"])
