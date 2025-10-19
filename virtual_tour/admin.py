from django.contrib import admin
from django.utils.html import format_html
from .models import CampusLocation


@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'image_preview')
    list_editable = ('order',)  # Allows reordering directly in the list
    search_fields = ('name', 'description')
    ordering = ('order',)
    readonly_fields = ('image_preview',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'order', 'image_360', 'image_preview')
        }),
    )

    def image_preview(self, obj):
        if obj.image_360:
            return format_html('<img src="{}" width="150" style="object-fit: cover;" />', obj.image_360.url)
        return "(No image)"
    image_preview.short_description = "360° Image Preview"