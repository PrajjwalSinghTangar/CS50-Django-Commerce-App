from django.contrib import admin

# Register your models here.
from .models import Bidding, User,Category,Listing, WatchList,Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(WatchList)
admin.site.register(Bidding)
admin.site.register(Comment)