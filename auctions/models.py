from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userBid")
    bid = models.IntegerField(default=0)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    initial_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name="initialBid" )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    url = models.CharField(max_length=2000, null=True)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchList")
    counter = models.IntegerField(default=1)

    def __str__(self):
        return self.title



class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listingComment")
    listingComment = models.CharField(max_length=300) 

    def __str__(self):
        return f"{self.author} comment in {self.listing}"


