from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import LocationForm
from .models import Location


# Create your views here.
class MapView(TemplateView):
    template_name = "location/map.html"


class LocationCreateView(LoginRequiredMixin, CreateView):
    form_class = LocationForm
    template_name = "location/location_create_form.html"
    success_url = reverse_lazy("location:map")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationDetailView(DetailView):
    template_name = "location/location_detail.html"
    model = Location


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "location/location_update_form.html"
    model = Location
    fields = ["name", "description"]

    def get_success_url(self):
        return reverse_lazy("location:location_detail", kwargs={"pk": self.object.pk})
