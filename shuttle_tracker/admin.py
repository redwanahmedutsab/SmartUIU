from django.contrib import admin
from .models import Route, LiveLocation


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Show route name in the admin list
    search_fields = ('name',)  # Add search functionality
