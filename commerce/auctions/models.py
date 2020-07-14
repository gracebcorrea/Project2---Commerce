from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Items(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=60)
    picture = models.CharField(max_length=60) #Name of the picture saved on static folder
    price = models.DecimalField()
    finalprice = models.DecimalFieldc()
    def __str__(self):
        return f"{self.code} ({self.name}) ({self.description}) ({self.picture}) ({self.price}) ({self.finalprice}) "

class Bids(models.Model):
    code = models.CharField(max_length=5)  #item code, the same as in Items
    user = models.CharField(max_length=25)
    userbid = models.DecimalField()
    def __str__(self):
        return f"{self.code} ({self.user}) ({self.userbid })"

        
