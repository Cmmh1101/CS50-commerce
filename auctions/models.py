from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return self.categoryName

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    initial_bid = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    url = models.CharField(max_length=2000, null=True)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchList")

    def __str__(self):
        return self.title

# class Bid(models.Model):
#     pass

# class Comment(models.Model):
#     pass


