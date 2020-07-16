from django.contrib import admin

#from django.contrib import admin

from .models import Listings, Categories, ActiveListings, Bids, Comments, Watchlist,SoldTo
# Register your models here.

#class FlightAdmin(admin.ModelAdmin):
#    list_display = ("__str__", "duration")

class Admin(admin.ModelAdmin):
    filter_horizontal = ("comerce",)


admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(ActiveListings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
admin.site.register(SoldTo)

#admin.site.register(Passenger, PassengerAdmin)
