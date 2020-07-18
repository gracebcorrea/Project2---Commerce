from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from . import views


#app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("Bids", views.Bids_view, name="Bids"),
    path("Categories", views.Categories_view, name="Categories"),
    path("CategoryShow", views.CategoryShow_view, name="CategoryShow"),
    path("CreateListings", views.CreateListings_view, name="CreateListings"),
    path("Listings", views.Listings_view, name="Listings"),
    path("Comments", views.Comments_view, name="Comments"), #vinculado a bids
    path("Watchlist", views.Watchlist_view, name="Watchlist"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
