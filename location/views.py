from typing import List

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.shortcuts import redirect, render
from django.urls import URLPattern, get_resolver, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
    UpdateView,
)

from .forms import CommentForm, LocationForm, PhotoForm
from .models import Like, Location


class MapView(TemplateView):
    template_name = "location/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 全てのLocationオブジェクト（HTML用）
        context["locations"] = Location.objects.order_by("-likes_count")

        # 全てのLocationオブジェクトのJSON（js用）
        context["locations_data"] = serializers.serialize(
            "json", Location.objects.all()
        )

        # locationアプリのURL
        app_url = {}
        url_obj = self.get_patterns("location")
        urlpatterns = url_obj.urlpatterns
        for url_pattern in urlpatterns:
            if hasattr(url_pattern, "name"):
                app_url[url_pattern.name] = "/location/" + str(url_pattern.pattern)
        context["location_urls"] = app_url

        return context

    def get_patterns(self, app: str) -> List[URLPattern]:
        """locationアプリのURLパターンを取得

        Args:
            app (str): アプリ名

        Returns:
            List[URLPattern]: アプリのURLパターンのリスト
        """
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

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     location = form.save()

    #     photo_form = PhotoForm(self.request.POST, self.request.FILES)
    #     if photo_form.is_valid():
    #         photo = photo_form.save(commit=False)
    #         photo.user = self.request.user
    #         photo.location = location
    #         photo.save()

    #     return super().form_valid(form)

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

        user = self.request.user
        if user.is_authenticated:
            context["already_liked"] = location.likes.filter(user=user).exists()
        else:
            context["already_liked"] = False

        context["photos"] = location.photos.all()
        context["comment_form"] = CommentForm()
        context["photo_form"] = PhotoForm()
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

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     if self.request.POST and self.request.FILES:
    #         photo_form = PhotoForm(self.request.POST, self.request.FILES)
    #         if photo_form.is_valid():
    #             photo = photo_form.save(commit=False)
    #             photo.user = self.request.user
    #             photo.location = self.object
    #             photo.save()
    #     return response


class LocationDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete_confirmation.html"
    model = Location
    success_url = reverse_lazy("location:map")


class PhotoFormView(LoginRequiredMixin, CreateView):
    """フォトフォームからのPOSTリクエスト処理"""

    form_class = PhotoForm

    def get_success_url(self):

        return reverse_lazy("location:detail", kwargs={"pk": self.kwargs["pk"]})

    def get_template_names(self):
        """リクエストが送信されてきたURLによって動的にテンプレートを決定"""
        if self.request.path.endswith("detail/"):
            return ["location/detail.html"]
        elif self.request.path.endswith("create-form/"):
            return ["location/create_form.html"]

    def form_valid(self, form):
        if self.request.POST and self.request.FILES:
            form.instance.user = self.request.user
            form.instance.location = Location.objects.get(pk=self.kwargs["pk"])
            return super().form_valid(form)


class LikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = self.request.user
        location = Location.objects.get(pk=pk)

        like_exists = Like.objects.filter(user=user, location=location).exists()
        if not like_exists:
            Like.objects.create(user=user, location=location)
            location.likes_count += 1
        else:
            Like.objects.filter(user=user, location=location).delete()
            location.likes_count -= 1

        location.save()

        return redirect("location:detail", pk=pk)


class CommentFormView(LoginRequiredMixin, CreateView):
    """detail.html内コメントフォームからのPOSTリクエスト処理"""

    form_class = CommentForm
    template_name = "location/detail.html"

    def get_success_url(self):
        return reverse_lazy("location:detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.location = Location.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)
