from django.contrib import admin
from django.utils.html import format_html
from .models import ThesisMemberProfile


@admin.register(ThesisMemberProfile)
class ThesisMemberProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'email', 'department', 'thesis_supervisor', 'availability', 'created_at', 'updated_at'
    )
    list_filter = ('department', 'availability', 'thesis_supervisor', 'created_at')
    search_fields = ('user__username', 'name', 'email', 'university_id', 'skills', 'research_interests')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'name', 'email', 'university_id', 'department', 'thesis_supervisor')
        }),
        ('Research & Skills', {
            'fields': ('skills', 'research_interests', 'thesis_topic')
        }),
        ('Availability & Contact', {
            'fields': ('availability', 'contact_info')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_picture_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.profile_picture.url)
        return "(No image)"
    profile_picture_preview.short_description = "Profile Picture Preview"