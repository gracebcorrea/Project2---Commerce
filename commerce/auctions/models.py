from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from PIL import Image
from PIL.Image import core as _imaging

class User(AbstractUser):
    pass



"""
Models: Your application should have at least three models in addition to the User model:
one for auction listings, one for bids, and one for comments made on auction listings.
It’s up to you to decide what fields each model should have, and what the types of those
fields should be. You may have additional models if you would like.
"""
#Properties   table  auctions_ActiveListings
class Listings(models.Model):
    Pcode = models.IntegerField() #key
    Ccode= models.IntegerField(help_text="Category House, Apartament, Commercial") #foreign key from PropTypes
    description = models.CharField(max_length=250)
    picture = models.ImageField(blank=True,upload_to=b"images") #Name of the picture saved on static folder
    price = models.FloatField(help_text="Just USD") #initial price
    def __str__(self):
        return f"({self.Pcode}) ({self.Ccode}) ({self.description}) ({self.picture}) ({self.price})"

#Properties types table auctions_Categories
class Categories(models.Model):
    Ccode=models.IntegerField() #key
    description = models.CharField(max_length=50)
    def __str__(self):
        return f"({self.Ccode}) ({self.description})"



#Auctions List  table auctions_Listings
class ActiveListings(models.Model):
    Lcode= models.IntegerField() #Key?
    Pcode = models.IntegerField() #foreignkey Property
    dateStart = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    duration = models.IntegerField(help_text="Duration expressed in days" )
    status = models.CharField(max_length=5) #to Begin, on , ended
    def __str__(self):
        return f"({self.Lcode})({self.Pcode}) ({self.dateStart}) ({self.duration}) ({self.status})"

#bids list  table auctions_Bids
class Bids(models.Model):
    Bcode = models.IntegerField() #pk
    Lcode= models.IntegerField() #foreignkey Listings
    Pcode = models.IntegerField()  #foreignkey Property
    user = models.CharField(max_length=25) #Who is going to buy
    Bthrow= models.IntegerField() #first throw, second , third....
    Bprice = models.FloatField(help_text="Just USD")# throw value
    def __str__(self):
        return f"({self.Bcode})({self.Lcode})({self.Pcode}) ({self.user}) ({self.Bthrow})  ({self.Bprice})"

#Comments table auctions_Comments
class Comments(models.Model):
    Ccode =models.IntegerField() #Key
    Lcode= models.IntegerField() #foreign key
    user = models.CharField(max_length=25)
    comment = models.CharField(max_length=250)
    def __str__(self):
        return f"({self.Ccode}) ({self.Lcode}) ({self.user}) ({self.comment})"


#Like Faforits???  table auctions_Watchlist
class Watchlist(models.Model):
    Wcode =models.IntegerField() #Key
    Lcode= models.IntegerField()
    user = models.CharField(max_length=25)
    def __str__(self):
        return f"({self.Wcode}) ({self.Lcode}) ({self.user}) "
