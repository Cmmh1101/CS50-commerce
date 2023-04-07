from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class ActionListings(models.Model):
#     title = models.CharField(max_length=64, blank=False, related_name="listings")
#     description = models.CharField(max_length=200)
#     initial_bid = models.IntegerField()
#     category = models.CharField(max_length=64)
#     url = models.CharField(max_length=200)

# class Bids(models.Model):
#     pass

# class Comments(models.Model):
#     pass


