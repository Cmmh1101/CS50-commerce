from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


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
            user = request.user
            selectedCategory = Category.objects.get(categoryName=category)

            listing = Listing(
                title = title,
                description = description,
                initial_bid =float(initial_bid),
                category = selectedCategory,
                url = url,
                owner = user
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
            "categories": categories
        })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    # for car in listing:
    #     car 
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user
    })