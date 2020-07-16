from django.contrib import admin

#from django.contrib import admin

from .models import Listings, Categories, ActiveListings, Bids, Comments, Watchlist
# Register your models here.


class Admin(admin.ModelAdmin):
    filter_horizontal = ("comerce",)


admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(ActiveListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)


#admin.site.register(Admin,Admin)
