from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LocationForm


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
