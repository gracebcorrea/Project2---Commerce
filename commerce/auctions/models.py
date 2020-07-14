from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Models(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=60)
    price = models.Numeric()
    finalprice = models.Numeric()
    picture = models.CharField(max_length=60)
