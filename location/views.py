from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render
from django.urls import URLPattern, get_resolver, reverse, reverse_lazy
from django.urls.exceptions import NoReverseMatch
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .forms import LocationForm
from .models import Location


# Create your views here.
class MapView(TemplateView):
    template_name = "location/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locations_data"] = serializers.serialize(
            "json", Location.objects.all()
        )
        context["locations"] = Location.objects.all()

        # locationアプリのurlオブジェクトを取得
        app_url = {}
        url_obj = self.get_patterns("location")
        urlpatterns = url_obj.urlpatterns
        for url_pattern in urlpatterns:
            if hasattr(url_pattern, "name"):
                app_url[url_pattern.name] = str(url_pattern.pattern)
        context["location_urls"] = app_url

        return context

    def get_patterns(self, app: str) -> List[URLPattern]:
        for pattern in get_resolver().url_patterns:
            if getattr(pattern, "app_name", "") == app:
                return pattern.urlconf_name


class LocationCreateView(LoginRequiredMixin, CreateView):
    form_class = LocationForm
    template_name = "location/location_create_form.html"
    success_url = reverse_lazy("location:map")

    def get_initial(self):
        initial = super().get_initial()
        lat = self.request.GET.get("lat")
        lng = self.request.GET.get("lng")

        if lat and lng:
            initial["latitude"] = lat
            initial["longitude"] = lng

        return initial

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


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete_confirmation.html"
    model = Location
    success_url = reverse_lazy("location:map")
