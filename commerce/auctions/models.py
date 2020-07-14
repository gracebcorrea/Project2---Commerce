from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#Properties  register
class Property(models.Model):
    Pcode = models.CharField(max_length=5) #key
    type = models.CharField(help_text="House, Apartament, Commercial",max_length=2) #foreign key from PropTypes
    size = models.DecimalField(max_digits=6, decimal_places=2) #m**2
    description = models.CharField(max_length=250)
    picture = models.CharField(max_length=60) #Name of the picture saved on static folder
    price = models.DecimalField(help_text="Just USD", max_digits=9, decimal_places=2) #initial price
    def __str__(self):
        return f"({self.Pcode}) ({self.type}) ({self.size}) ({self.description}) ({self.picture}) ({self.price})"

#Auctions List
class Listings(models.Model):
    Lcode= models.IntegerField() #Key?
    user = models.CharField(help_text="User responsable for the Listings",max_length=25)
    dateStart = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    duration = models.IntegerField(help_text="Duration expressed in days" )
    Pcode = models.CharField(max_length=5) #foreignkey Property
    status = models.CharField(max_length=5) #to Begin, on , ended
    def __str__(self):
        return f"({self.lcode}) ({self.user}) ({self.dateStart}) ({self.dateEnd }) ({self.duration}) ({self.Pcode})({self.status})"

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
    Listcode= models.IntegerField() #foreign key
    user = models.CharField(max_length=25)
    comment = models.CharField(max_length=250)
    def __str__(self):
        return f"({self.Comcode}) ({self.Listcode}) ({self.user}) ({self.comment})"
#Auction Results
class Soldto(models.Model):
    Lcode= models.IntegerField()
    Pcode = models.CharField(max_length=5)
    user  = models.CharField(max_length=25)
    date = models.DateField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    bidprice = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=5) #on , ended

def __str__(self):
    return f"({self.Lcode})({self.Pcode}) ({self.user}) ({self.date})  ({self.bidprice})  ({self.status})"
