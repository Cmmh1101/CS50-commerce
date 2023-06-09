from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("category", views.category, name="category"),
    path("category/<str:category>", views.filteredListings, name="filteredListings"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("updateBid/<int:listing_id>", views.updateBid, name="updateBid"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction")
]
