from django.contrib import admin

#from django.contrib import admin

from .models import Listings, Categories, Bids, Comments, Watchlist
# Register your models here.


class Admin(admin.ModelAdmin):
    filter_horizontal = ("commerce",)


admin.site.register(Listings)
admin.site.register(Categories)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)


#admin.site.register(Admin,Admin)
