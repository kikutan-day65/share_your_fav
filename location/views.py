from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .forms import LocationForm
from .models import Like, Location


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
                "created_at",
                "updated_at",
            )
        )
        data_url = reverse("map:location_data", kwargs={"pk": 0})
        context = {
            "locations": locations,
            "data_url": data_url,
        }
        return render(request, self.template_name, context)


class LocationDataView(View):
    template_name = "location/location_data.html"

    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        likes_count = location.like_set.count()
        user_liked = False
        if request.user.is_authenticated:
            user_liked = Like.objects.filter(
                user=request.user, location=location
            ).exists()

        context = {
            "location": location,
            "likes_count": likes_count,
            "user_liked": user_liked,
        }
        return render(request, self.template_name, context)


class LocationFormView(CreateView):
    model = Location
    form_class = LocationForm
    template_name = "location/location_form.html"
    success_url = reverse_lazy("map:map")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LikeView(View):
    def post(self, request, location_id):
        location = get_object_or_404(Location, id=location_id)
        user = request.user

        # Check if the user has already liked
        like, created = Like.objects.get_or_create(user=user, location=location)

        if not created:
            like.delete()
            print(f"{user.username} unliked {location.name}.")
        else:
            print(f"{user.username} liked {location.name}.")

        return redirect("map:map")
