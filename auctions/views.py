from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "activeListings": activeListings,
        "categories": categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def add(request):
        if request.method == "GET":
            categories = Category.objects.all()
            return render(request, "auctions/add.html", {
                "categories": categories
            })
        else:
            title = request.POST["title"]
            description = request.POST["description"]
            initial_bid = request.POST["initial-bid"]
            category = request.POST["category"]
            url = request.POST["url"]
            currentUser = request.user
            bid = Bid(bid=float(initial_bid), user=currentUser)
            bid.save()
            selectedCategory = Category.objects.get(categoryName=category)

            listing = Listing(
                title = title,
                description = description,
                initial_bid = bid,
                category = selectedCategory,
                url = url,
                owner = currentUser
            )

            listing.save()

            return HttpResponseRedirect(reverse("index"))

def category(request):
    if request.method == "POST": 
        category_selected = request.POST['category']
        category = Category.objects.get(categoryName=category_selected)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "activeListings": activeListings,
            "categories": categories,
            "activeFilter": category
        })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    isInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    isListingOwner = request.user == listing.owner
    # bidWinner = 
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "isInWatchlist": isInWatchlist,
        "comments": comments,
        "isListingOwner": isListingOwner
    })

def removeWatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def addWatchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def watchlist(request):
    currUser = request.user
    listings = currUser.listingWatchList.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def addComment(request, listing_id):
    currUser = request.user
    listing = Listing.objects.get(pk=listing_id)
    message = request.POST['comment']
    isInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)

    newMessage = Comment(
        author = currUser,
        listing = listing,
        listingComment = message
    )
    newMessage.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": currUser,
        "isInWatchlist": isInWatchlist,
        "comments": comments

    })

def updateBid(request, listing_id):
    new_bid = request.POST.get("new-bid", False)
    listing = Listing.objects.get(pk=listing_id)
    currentUser = request.user
    isInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    isListingOwner = request.user == listing.owner
    if int(new_bid) > listing.initial_bid.bid:
        updatedBid = Bid(bid=int(new_bid), user=currentUser)
        updatedBid.save()
        listing.initial_bid = updatedBid
        listing.save()
        print(new_bid)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your bid was suscessfully updated!",
            "update": True,
            "isListingOwner": isListingOwner
        })
    else:
        print(new_bid)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "The new bid should be grater than the current. Please try again!",
            "update": False,
            "isListingOwner": isListingOwner
        })

def closeAuction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    isInWatchlist = request.user in listing.watchlist.all()
    comments = Comment.objects.filter(listing=listing)
    isListingOwner = request.user == listing.owner
    listing.isActive = False
    listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": request.user,
        "isInWatchlist": isInWatchlist,
        "comments": comments,
        "isListingOwner": isListingOwner,
        "message": "Congrats!! You successfully closed your auction",
        "update": True
    })


