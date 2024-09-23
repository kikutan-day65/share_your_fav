from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import LocationForm
from .models import Location


# Create your views here.
class Map(View):
    template_name = "location/map.html"

    def get(self, request):
        locations = list(
            Location.objects.values(
                "id",
                "name",
                "latitude",
                "longitude",
                "description",
                "like_count",
                "dislike_count",
                "created_at",
                "updated_at",
            )
        )
        context = {"locations": locations}
        return render(request, self.template_name, context)


class LocationFormView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = "location/location_form.html"
    success_url = reverse_lazy("map:map")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
