from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Route, LiveLocation
import json


# Home page showing all routes
def home(request):
    routes = Route.objects.all()
    return render(request, 'shuttle_tracker/shuttle_tracker_home.html', {'routes': routes})


# Shuttle tracker page
def shuttle_tracker(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    return render(request, 'shuttle_tracker/shuttle_tracker.html', {'route': route})


# API: Get live locations
def live_locations_api(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    locations = LiveLocation.active_locations(route)
    data = {
        "locations": [
            {
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "display_name": loc.display_name,
                "user_id": loc.user.id,
            }
            for loc in locations
        ]
    }
    return JsonResponse(data)


# API: Start Sharing
@csrf_exempt
def share_location_api(request, route_id):
    if request.method == "POST" and request.user.is_authenticated:
        route = get_object_or_404(Route, id=route_id)
        body = json.loads(request.body)
        choice = body.get("choice")

        display_name = request.user.username if choice == "name" else "Anonymous"
        latitude = body.get("latitude", 23.7808875)
        longitude = body.get("longitude", 90.2792371)

        loc, created = LiveLocation.objects.update_or_create(
            user=request.user,
            route=route,
            defaults={
                "latitude": latitude,
                "longitude": longitude,
                "is_sharing": True,
                "display_name": display_name,
            }
        )
        return JsonResponse({"success": True, "display_name": display_name})

    return JsonResponse({"error": "Invalid request"}, status=400)


# API: Stop Sharing
@csrf_exempt
def stop_location_api(request, route_id):
    if request.method == "POST" and request.user.is_authenticated:
        route = get_object_or_404(Route, id=route_id)
        LiveLocation.objects.filter(user=request.user, route=route).update(is_sharing=False)
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


# API: Check if current user is sharing location on a route
from django.contrib.auth.decorators import login_required


@login_required
def check_sharing_status(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    is_sharing = LiveLocation.objects.filter(user=request.user, route=route, is_sharing=True).exists()
    return JsonResponse({"is_sharing": is_sharing})
