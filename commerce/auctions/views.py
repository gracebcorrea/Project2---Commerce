import sqlite3, datetime, os, os.path
import time
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse,include, path
from django.contrib import admin
from django import forms

from . import views

from .models import User, Listings, Categories, Bids, Comments, Watchlist


class BidForm(forms.Form):
    Bid_price= forms.FloatField(label="Your Offer")

class CommentForm(forms.Form):
    C_Ccomment = forms.CharField(label='Your Comment',widget=forms.Textarea)

class ChangeStatusForm(forms.Form):
    CHOICES = [('Active','Active - Receiving Bids'), ('To Begin','To Begin - De Auction didn´t start yet'),('Closed','Closed - The seller gave up the auction'), ('Sold','Sold')]
    L_Lstatus = forms.ChoiceField(label='Do You Want to Change Status?',widget=forms.Select, choices=CHOICES)

class AddWatch(forms.Form):
    AddWatch = forms.IntegerField(initial=1,widget=forms.HiddenInput)

class RemoveWatch(forms.Form):
    RemoveWatch = forms.IntegerField(initial=0,widget=forms.HiddenInput)


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
@login_required
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




@login_required
def Categories_view(request):
    d = datetime.now()

    context= {
        "d": d,
        "Categories": Categories.objects.all(),
        }
    return render(request, "auctions/Categories.html", context)

#resolver problema
@login_required
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

If the item is already on the watchlist, the user should be able to remove it.

"""
#List Listings details -  All
@login_required
def Listingspage_view(request):
    d = datetime.now()
    context={
       "d": d,
       "Listings": Listings.objects.all(),
    }
    return render(request,"auctions/Listingspage.html", context)



@login_required
def Bids_view(request, Btitle):
    B_title =Btitle
    d = datetime.now()

    if request.user.is_authenticated:
        Username= request.user.username


    #take data from desired listing
    L_data = Listings.objects.filter(Ltitle=B_title)
    Status = L_data[0].Lstatus

    Lfilter = Listings.objects.filter(Ltitle=B_title).values('id' , 'Lprice')
    for Search_id in Lfilter:
        Lid_value = int(Search_id['id'])
        Lprice = float(Search_id['Lprice'])

    #Take Watchlist
    W_data = Watchlist.objects.filter(Lcode__Ltitle=B_title,user=Username)

    #Take comments for this listing
    C_data = Comments.objects.filter(Lcode__Ltitle=B_title)

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

        FB = BidForm(request.POST)
        FC = CommentForm(request.POST)
        FChange = ChangeStatusForm(request.POST)
        FAdd = AddWatch(request.POST)
        FRemove = RemoveWatch(request.POST)

        #New BID
        if FB.is_valid():

            B_user = Username
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
                    "Btitle":B_title,
                    "L_data":L_data,
                    "B_data":B_data,
                    "W_data":W_data,
                    "C_data":C_data,
                    "BestOffer":BestOffer,
                    "Status":Status,
                    "Winner":Winner,
                    "CommentForm": CommentForm(),
                    "BidForm":BidForm(),
                    "ChangeStatusForm":ChangeStatusForm(),
                    "AddWatch":AddWatch(),
                    "RemoveWatch":RemoveWatch(),
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
                    "Btitle":B_title,
                    "L_data":L_data,
                    "B_data":B_data,
                    "W_data":W_data,
                    "C_data":C_data,
                    "BestOffer":BestOffer,
                    "Status":Status,
                    "Winner":Winner,
                    "CommentForm": CommentForm(),
                    "BidForm":BidForm(),
                    "ChangeStatusForm":ChangeStatusForm(),
                    "AddWatch":AddWatch(),
                    "RemoveWatch":RemoveWatch(),

                }
                return render(request, "auctions/BidsDetail.html", context)

            except :
                return HttpResponse(" Something Wrong tyring to save Bid")

        if FC.is_valid():
            C_Cuser= Username
            C_comment =  FC.cleaned_data["C_Ccomment"]
            C_Lcode = int(Lid_value)
            C_Cdate = time.strftime("%Y-%m-%d")

            try:

                NewComment = Comments(Cdate=C_Cdate, Cuser=C_Cuser,Ccomment=C_comment, Lcode_id=C_Lcode )
                NewComment.save()

                C_data=Comments.objects.filter(Lcode__Ltitle=B_title)

                context = {
                    "msgcomment" :"New comment saved!",
                    "d":d,
                    "Btitle":B_title,
                    "L_data":L_data,
                    "B_data":B_data,
                    "W_data":W_data,
                    "C_data":C_data,
                    "BestOffer":BestOffer,
                    "Status":Status,
                    "Winner":Winner,
                    "CommentForm": CommentForm(),
                    "BidForm":BidForm(),
                    "ChangeStatusForm":ChangeStatusForm(),
                    "AddWatch":AddWatch(),
                    "RemoveWatch":RemoveWatch(),
                }
                return render(request, "auctions/BidsDetail.html", context)
            except  :
                return HttpResponse( "ERROR trying to save new comment."  )

        if FChange.is_valid():

            New_Status =FChange.cleaned_data
            SelectedStatus = request.POST.getlist('L_Lstatus')
            for S in SelectedStatus:
                NewStatus = S[0:8]

            try:
                Updatelistings = Listings.objects.get(Ltitle=B_title)
                Updatelistings.Lstatus = NewStatus
                Updatelistings.save()

                L_data = Listings.objects.filter(Ltitle=B_title)
                Status= L_data[0].Lstatus

                context = {
                    "msgstatus" :"New Status saved!",
                    "d":d,
                    "Btitle":B_title,
                    "L_data":L_data,
                    "B_data":B_data,
                    "W_data":W_data,
                    "C_data":C_data,
                    "BestOffer":BestOffer,
                    "Status":Status,
                    "Winner":Winner,
                    "CommentForm": CommentForm(),
                    "BidForm":BidForm(),
                    "ChangeStatusForm":ChangeStatusForm(),
                    "AddWatch":AddWatch(),
                    "RemoveWatch":RemoveWatch(),

                }
                return render(request, "auctions/BidsDetail.html", context)
            except:
                return HttpResponse( "ERROR trying to update Listing Status" )

        if FAdd.is_valid():

            Add_W = FAdd.cleaned_data

            try:
                if Watchlist.objects.filter(Lcode__Ltitle=B_title,user=Username):
                   msgAdd = "This Item is already Watched."

                else:
                    Watchlist_create= Watchlist.objects.create(Lcode_id=Lid_value,user=Username,Wflag=1)
                    Watchlist_create.save()


                    W_data = Watchlist.objects.filter(Lcode__Ltitle=B_title,user=Username)
                    msgAdd = "Saved To WatchList."

                context = {
            
                    "d":d,
                    "Btitle":B_title,
                    "L_data":L_data,
                    "B_data":B_data,
                    "W_data":W_data,
                    "C_data":C_data,
                    "BestOffer":BestOffer,
                    "Status":Status,
                    "Winner":Winner,
                    "CommentForm": CommentForm(),
                    "BidForm":BidForm(),
                    "ChangeStatusForm":ChangeStatusForm(),
                    "AddWatch":AddWatch(),
                    "RemoveWatch":RemoveWatch(),
                }
                return render(request, "auctions/BidsDetail.html", context)
            except:
                return HttpResponse( "ERROR trying to ADD to Whatchlist"  )


        if FRemove.is_valid():

            Remove_W =FRemove.cleaned_data

            try:

                if Watchlist.objects.filter(Lcode_id=Lid_value,user=Username,Wflag=1):
                    W_remove=Watchlist.objects.filter(Lcode_id=Lid_value,user=Username,Wflag=1)
                    W_remove.delete()

                print("TRYING TO DELETE :",Username, Lid_value  )

                FRemove.save()
                W_data=Watchlist.objects.filter(Lcode__Ltitle=B_title,user=Username)

                context = {

                    "d":d,
                    "Btitle" :B_title,
                    "L_data" :L_data,
                    "B_data" :B_data,
                    "W_data" :W_data,
                    "C_data" :C_data,
                    "BestOffer" :BestOffer,
                    "Status" :Status,
                    "Winner" :Winner,
                    "CommentForm" : CommentForm(),
                    "BidForm" :BidForm(),
                    "ChangeStatusForm" :ChangeStatusForm(),
                    "AddWatch" :AddWatch(),
                    "RemoveWatch" :RemoveWatch(),
                }
                return render(request, "auctions/BidsDetail.html", context)
            except:
                return HttpResponse( "ERROR trying Remove from Watchlist" )



    else:
        context = {

            "d":d,
            "Btitle":B_title,
            "L_data":L_data,
            "B_data":B_data,
            "W_data":W_data,
            "C_data":C_data,
            "BestOffer":BestOffer,
            "Status":Status,
            "Winner":Winner,
            "BidForm":BidForm(),
            "CommentForm": CommentForm(),
            "ChangeStatusForm" :ChangeStatusForm(),
            "AddWatch" : AddWatch(),
            "RemoveWatch": RemoveWatch(),
        }
        return render(request, "auctions/BidsDetail.html", context)



@login_required
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
