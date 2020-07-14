from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("property", views.property, name="property"),
    path("bids", views.bids, name="bids"),
    path("listings", views.listings, name="listings"),
    path("comments", views.comments, name="comments"),
    path("soldto", views.soldto, name="soldto"),

]
