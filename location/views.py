from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import render
from django.urls import URLPattern, get_resolver, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .forms import LocationForm, PhotoForm
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
                app_url[url_pattern.name] = "/location/" + str(url_pattern.pattern)
        context["location_urls"] = app_url

        return context

    def get_patterns(self, app: str) -> List[URLPattern]:
        for pattern in get_resolver().url_patterns:
            if getattr(pattern, "app_name", "") == app:
                return pattern.urlconf_name


class LocationCreateView(LoginRequiredMixin, CreateView):
    form_class = LocationForm
    template_name = "location/create_form.html"
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
        location = form.save()

        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.user = self.request.user
            photo.location = location
            photo.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo_form"] = PhotoForm()
        return context


class LocationDetailView(DetailView):
    template_name = "location/detail.html"
    model = Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.object
        context["photos"] = location.photos.all()
        return context


class LocationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "location/update_form.html"
    model = Location
    fields = ["name", "description"]

    def get_success_url(self):
        return reverse_lazy("location:detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo_form"] = PhotoForm()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.user = self.request.user
            photo.location = self.object
            photo.save()
        return response


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete_confirmation.html"
    model = Location
    success_url = reverse_lazy("location:map")
