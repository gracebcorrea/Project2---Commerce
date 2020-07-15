from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("ActiveListings", views.ActiveListings, name="ActiveListings"),
    path("Listings", views.Listings, name="Listings"),
    path("Bids", views.Bids, name="Bids"),
    path("Comments", views.Comments, name="Comments"), #vinculado a bids
    path("SoldTo", views.SoldTo, name="SoldTo"),
    path("CreateListings", views.CreateListings, name="CreateListings"),
    path("Watchlist", views.Watchlist, name="Watchlist"),

]
