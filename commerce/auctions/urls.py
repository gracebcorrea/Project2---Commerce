from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import index, login_view,logout_view,register
from .views import CreateListings_view, Listingspage_view,  Bids_view
from .views import Watchlist_view, Categories_view, CategoryShow_view


app_name = 'auctions'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    path('index', views.index, name='index'),
    path('CreateListings', views.CreateListings_view, name='CreateListings'),
    path('Listingspage', views.Listingspage_view, name='Listingspage'),
    path('Bid/<str:Btitle>', views.Bids_view, name='BidsDetail'),
    path('Categories', views.Categories_view, name='Categories'),
    path('Category/<str:C_description>', views.CategoryShow_view, name='CategoryShow'),
    path('Watchlist', views.Watchlist_view, name='Watchlist'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
