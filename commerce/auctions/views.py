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


class BidForm(forms.Form):
    Bid_price= forms.FloatField(label="Offer a Bid")

class CommentForm(forms.Form):
    C_Ccomment = forms.CharField(label = "Write a comment:")


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
        Ccode=int(request.POST["Ccode"])
        Ldescription=request.POST["Ldescription"]
        Lprice=float(request.POST["Lprice"].replace(',', '.'))
        Ldatestart=request.POST["Ldatestart"]
        Lduration=request.POST["Lduration"]
        Luser=request.POST["Luser"]
        Lstatus=request.POST["Lstatus"]
        Limage="media/"+str(request.POST["Limage"])


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




def Watchlist_add(Btitle,user):
    W_Lcode=Lcode
    W_user=user
    try:
        Watchlist_create= Watchlist.objects.create(Lcode=W_Lcode,user=W_user,Wflag=1)
        Watchlist_create.save()
    except IntegrityError:
        return HttpResponse(" Integryty Error tryng to save new watchlist item")

    return None

def Watchlist_remove(Btitle,user):
    W_Lcode=Lcode
    W_user=user

    try:
        W_remove=Watchlist.objects.delete(Lcode=W_Lcode,user=W_user).delete()
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
    }
    return render(request,"auctions/Listingspage.html", context)




def Bids_view(request, Btitle):
    B_title =Btitle
    d = datetime.now()

    #take data from desired listing
    L_data = Listings.objects.filter(Ltitle=B_title)
    Status = L_data[0].Lstatus

    Lfilter = Listings.objects.filter(Ltitle=B_title).values('id' , 'Lprice','Lstatus')
    for Search_id in Lfilter:
        Lid_value = int(Search_id['id'])
        Lprice = float(Search_id['Lprice'])

    #Take Watchlist
    W_data=Watchlist.objects.filter(Lcode__Ltitle=B_title)

    #Take comments for this listing
    C_data=Comments.objects.filter(Lcode__Ltitle=B_title)

    #take all bids for this listing
    B_data = Bids.objects.filter(Lcode__Ltitle=B_title)
    Last_Bid = Bids.objects.filter(Lcode__Ltitle=B_title).order_by('-Bprice')[:1]
    if Last_Bid:
        BestOffer = Last_Bid[0].Bprice
        Winner = Last_Bid[0].Buser
    else:
        BestOffer = 0
        Winner = "No Offers Yet"

    if request.method == "POST":
        #User= request.POST["User"]
        User= request.POST.get('User')
        FB = BidForm(request.POST)
        FC = CommentForm(request.POST)

        if FB.is_valid():
            B_user = User
            B_price =FB.cleaned_data["Bid_price"]
            B_date = time.strftime("%Y-%m-%d")
            Lances= Bids.objects.filter(Lcode_id=Lid_value).values('Bthrow', 'Bprice').order_by('Bthrow')
            if len(Lances):
                for L in Lances:
                   N_Bthrow = L['Bthrow']
                   N_Bprice = float(L['Bprice'])

                B_throw = N_Bthrow + 1

            else:
                B_throw = 1
                N_Bprice= Lprice

            if (B_price <  Lprice) or (B_price <  N_Bprice):
                msgbids= "EROR: A bid must be greater than or equal to the original amount and greater than the last bid, if any."

                context={
                "msgbids":msgbids ,
                "d":d,
                "Btitle" : Btitle,
                "L_data" :L_data,
                "Status":Status,
                "B_data" :B_data,
                "BestOffer":BestOffer,
                "Winner":Winner,
                "W_data" :W_data,
                "C_data":C_data,
                "BidForm": FB,
                 }
                return render(request, "auctions/BidsDetail.html", context)

            try:

                NewBid = Bids(Lcode_id=Lid_value , Buser=B_user , Bthrow=B_throw, Bprice=B_price ,Bdate=B_date )
                NewBid.save()

                #get data with new bid to show on form
                B_data=Bids.objects.filter(Lcode__Ltitle=B_title)
                msgbids ="New Bid Saved, Good Luck!"
                context={
                    "msgbids":msgbids ,
                    "d":d,
                    "Btitle" : Btitle,
                    "L_data" :L_data,
                    "Status":Status,
                    "B_data" :B_data,
                    "BestOffer":BestOffer,
                    "Winner":Winner,
                    "W_data" :W_data,
                    "C_data":C_data,
                    "BidForm": FB,
                }
                return render(request, "auctions/BidsDetail.html", context)

            except :
                return HttpResponse(" Something Wrong tyring to save Bid")

        if FC.is_valid():
            C_Cuser= User
            C_comment =  FC.cleaned_data["C_Ccomment"]
            C_Lcode = Lid_value
            C_Cdate = time.strftime("%Y-%m-%d")

            try:

                print ("Vou salvar novo comentario :", C_Lcode, C_Cdate, C_Cuser ,C_comment )

                NewComment = Comments(Cdate=C_Cdate, Cuser=C_Cuser,Ccomment=C_comment, Lcode_id=C_Lcode )
                NewComment.user()

                NewC_data=Comments.objects.filter(Lcode__Ltitle=B_title)
                print(NewC_data)

                context = {
                    "msgcomment" :"New comment saved!",
                    "d":d,
                    "Btitle" : Btitle,
                    "L_data" :L_data,
                    "Status":Status,
                    "B_data" :B_data,
                    "BestOffer":BestOffer,
                    "Winner":Winner,
                    "W_data" :W_data,
                    "C_data":NewC_data,
                    "CommentForm": FC,
                }
                return render(request, "auctions/BidsDetail.html", context)

            except FieldError:
                return HttpResponse(" Something Wrong FieldError New Comment")
        



    else:
        context = {

            "d":d,
            "Btitle":B_title,
            "L_data":L_data,
            "Status":Status,
            "B_data":B_data,
            "W_data":W_data,
            "C_data":C_data,
            "BidForm":BidForm(),
            "CommentForm": CommentForm(),
            "BestOffer":BestOffer,
            "Winner":Winner,
        }
        return render(request, "auctions/BidsDetail.html", context)
