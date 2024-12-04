from django.contrib import admin

from .models import Like, Location, Photo, Comment

# Register your models here.
admin.site.register(Location)
admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Comment)
