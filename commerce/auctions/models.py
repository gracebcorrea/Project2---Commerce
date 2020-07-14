from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from PIL.Image import core as _imaging

class User(AbstractUser):
    pass

#Properties  register
class ActiveListings(models.Model):
    Pcode = models.CharField(max_length=5) #key
    Ccode=models.IntegerField(help_text="Category House, Apartament, Commercial") #foreign key from PropTypes
    description = models.CharField(max_length=250)
    picture = models.ImageField() #Name of the picture saved on static folder
    price = models.DecimalField(help_text="Just USD", max_digits=9, decimal_places=2) #initial price
    def __str__(self):
        return f"({self.Pcode}) ({self.Ccode}) ({self.description}) ({self.picture}) ({self.price})"


class Categories(models.Model):
    Ccode=models.IntegerField()
    description = models.CharField(max_length=50)
    def __str__(self):
        return f"({self.Ccode}) ({self.description})"



#Auctions List
class Listings(models.Model):
    Lcode= models.IntegerField() #Key?
    Pcode = models.CharField(max_length=5) #foreignkey Property
    dateStart = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    duration = models.IntegerField(help_text="Duration expressed in days" )
    status = models.CharField(max_length=5) #to Begin, on , ended
    def __str__(self):
        return f"({self.lcode})({self.Pcode}) ({self.dateStart}) ({self.duration}) ({self.status})"

#bids list
class Bids(models.Model):
    Lcode= models.IntegerField() #foreignkey Listings
    Pcode = models.CharField(max_length=5)  #foreignkey Property
    user = models.CharField(max_length=25) #Who is going to buy
    bidnumber= models.IntegerField() #first throw, second , third....
    bidprice = models.DecimalField(max_digits=9, decimal_places=2)# throw value
    def __str__(self):
        return f"({self.Lcode})({self.Pcode}) ({self.user}) ({self.bidnumber})  ({self.bidprice})"

#Comments
class Comments(models.Model):
    Comcode =models.IntegerField() #Key
    Lcode= models.IntegerField() #foreign key
    user = models.CharField(max_length=25)
    comment = models.CharField(max_length=250)
    def __str__(self):
        return f"({self.Comcode}) ({self.Lcode}) ({self.user}) ({self.comment})"


#Like Faforits???
class Watchlist(models.Model):
    Wcode =models.IntegerField() #Key
    Lcode= models.IntegerField()
    user = models.CharField(max_length=25)
    def __str__(self):
        return f"({self.Wcode}) ({self.Lcode}) ({self.user}) "


#Auction Results - Vendido para...

class Soldto(models.Model):
    Lcode= models.IntegerField()
    Pcode = models.CharField(max_length=5)
    user  = models.CharField(max_length=25)
    date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    bidprice = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=5) #open or closed
    def __str__(self):
        return f"({self.Lcode})({self.Pcode}) ({self.user}) ({self.date})  ({self.bidprice})  ({self.status})"
