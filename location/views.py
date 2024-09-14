from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import LocationForm
from .models import Location


# Create your views here.
class Map(View):
    def get(self, request):
        return render(request, "location/map.html")


class LocationFormView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = "location/location_form.html"
    success_url = reverse_lazy("map:map")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
