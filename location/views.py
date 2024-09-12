from django.shortcuts import render
from django.views import View

from .forms import LocationForm


# Create your views here.
class Map(View):
    def get(self, request):
        return render(request, "location/map.html")


class LocationFormView(View):
    def get(self, request):
        form = LocationForm()
        context = {"form": form}
        return render(request, "location/location_form.html", context)

    def post(self, request):
        form = LocationForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, "location/location_form.html", context)
