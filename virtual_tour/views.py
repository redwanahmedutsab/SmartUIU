from django.shortcuts import render, get_object_or_404
from .models import CampusLocation


def tour_home(request):
    locations = CampusLocation.objects.all().order_by('order')
    return render(request, 'virtual_tour/virtual_tour_home.html', {'locations': locations})


def virtual_tour(request, location_id):
    location = get_object_or_404(CampusLocation, id=location_id)
    return render(request, 'virtual_tour/virtual_tour.html', {'location': location})
