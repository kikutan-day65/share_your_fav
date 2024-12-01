from django.contrib import admin

from .models import Like, Location, Photo

# Register your models here.
admin.site.register(Location)
admin.site.register(Photo)
admin.site.register(Like)
