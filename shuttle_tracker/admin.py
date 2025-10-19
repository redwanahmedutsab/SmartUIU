from django.contrib import admin
from .models import Route, LiveLocation


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(LiveLocation)
class LiveLocationAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'route', 'latitude', 'longitude', 'is_sharing', 'timestamp')
    list_filter = ('is_sharing', 'route', 'timestamp')
    search_fields = ('display_name', 'user__username', 'route__name')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    autocomplete_fields = ['user', 'route']

    actions = ['stop_sharing', 'start_sharing']

    @admin.action(description="Stop Sharing for selected users 🚫")
    def stop_sharing(self, request, queryset):
        updated = queryset.update(is_sharing=False)
        self.message_user(request, f"{updated} location(s) stopped sharing.")

    @admin.action(description="Start Sharing for selected users ✅")
    def start_sharing(self, request, queryset):
        updated = queryset.update(is_sharing=True)
        self.message_user(request, f"{updated} location(s) started sharing.")