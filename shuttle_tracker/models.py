from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LiveLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    is_sharing = models.BooleanField(default=True)
    display_name = models.CharField(max_length=100, default="Anonymous")

    def __str__(self):
        return f"{self.display_name} - {self.route.name}"

    @classmethod
    def active_locations(cls, route):
        """Return only active locations (last 30 minutes and sharing=True)."""
        cutoff = timezone.now() - timedelta(minutes=30)
        return cls.objects.filter(route=route, is_sharing=True, timestamp__gte=cutoff)
