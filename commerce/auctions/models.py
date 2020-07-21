from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from PIL import Image
from PIL.Image import core as _imaging

from django.conf import settings
from django.conf.urls.static import static

class User(AbstractUser):
    pass



"""
Models: Your application should have at least three models in addition to the User model:
one for auction listings, one for bids, and one for comments made on auction listings.
It’s up to you to decide what fields each model should have, and what the types of those
fields should be. You may have additional models if you would like.
"""
#Properties   table  auctions_Listings
class Listings(models.Model):
    STATUS = (
        ('Active', 'Active - Receiving Bids'),
        ('To Begin', 'To Begin - De Auction didn´t start yet'),
        ('Closed', 'Closed - The seller gave up the auction'),
        ('Sold', 'Sold'),
    )

    Ltitle = models.CharField(help_text="Choose a title for your listing",max_length=50)
    Ccode=models.IntegerField(help_text="Categories Ex: 1-Apartament,2-Commercial,3-Farm, 4-House ") #foreign key from PropTypes
    Ldescription = models.CharField(max_length=250)
    Lprice = models.FloatField(help_text="starting bid Just USD") #initial price
    Ldatestart = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>. for the auction start")
    Lduration = models.IntegerField(help_text="Duration expressed in days" )
    Luser = models.CharField(max_length=25)
    Limage= models.ImageField(upload_to="media", blank=True) #Name of the picture saved on static folder
    Lstatus = models.CharField(max_length=8, choices=STATUS )
    def __str__(self):
        return f"({self.Ltitle}) ({self.Lstatus}) "
#({self.Ccode}) ({self.Ldescription}) ({self.Lprice}) ({self.Ldatestart}) ({self.Lduration}) ({self.Luser})({self.Limage})
#Properties types table auctions_Categories
class Categories(models.Model):
    Ccode=models.IntegerField() #key
    Cdescription = models.CharField(max_length=50)
    def __str__(self):
        return f"({self.Ccode}) ({self.Cdescription})"



#bids list  table auctions_Bids
class Bids(models.Model):
    Lcode = models.ForeignKey(Listings, on_delete=models.CASCADE)
    Buser = models.CharField(max_length=25) #Who is going to buy
    Bthrow= models.IntegerField() #first throw, second , third....
    Bprice = models.FloatField(help_text="Just USD")# throw value
    Bdate = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    def __str__(self):
        return f"({self.Lcode})({self.Buser})({self.Bthrow}) ({self.Bprice}) ({self.Bdate})"

#Comments table auctions_Comments
class Comments(models.Model):
    Lcode = models.ForeignKey(Listings, on_delete=models.CASCADE)
    Luser  = models.CharField(max_length=25) #Who is selling
    Lcomment = models.CharField(max_length=250)
    Buser = models.CharField(max_length=25) #Who is buying
    Bcomment = models.CharField(max_length=250)
    def __str__(self):
        return f"({self.Lcode}) ({self.Luser }) ({self.Lcomment}) ({self.Buser}) ({self.Bcomment})"


#Like Faforits???  table auctions_Watchlist
class Watchlist(models.Model):
    Lcode = models.ForeignKey(Listings, on_delete=models.CASCADE)
    Wflag =models.IntegerField() #Key
    user = models.CharField(max_length=25)
    def __str__(self):
        return f"({self.Lcode}) ({self.Wflag}) ({self.user}) "
