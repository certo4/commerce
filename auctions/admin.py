from django.contrib import admin

# Register your models here.
from .models import User, Listing, Bid, Comment
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
