from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_name',
        'email',
        'mobile',
        'location',
        'time_date',
        'post_time',
        'post_status',
        'found_by_name',
    )
    list_filter = ('post_status', 'post_time', 'location')
    search_fields = ('item_name', 'email', 'mobile', 'location', 'found_by_name')
    readonly_fields = ('post_time',)
    ordering = ('-post_time',)
    list_per_page = 25

    fieldsets = (
        ('Item Information', {
            'fields': ('item_name', 'item_image', 'description')
        }),
        ('Contact & Location', {
            'fields': ('email', 'mobile', 'location', 'time_date')
        }),
        ('Status', {
            'fields': ('post_status', 'found_by_name')
        }),
        ('User Info', {
            'fields': ('user',)
        }),
        ('Meta Info', {
            'fields': ('post_time',)
        }),
    )

    actions = ['mark_as_found', 'mark_as_unfound']

    @admin.action(description="Mark selected items as Found ✅")
    def mark_as_found(self, request, queryset):
        updated = queryset.update(post_status=True)
        self.message_user(request, f"{updated} item(s) marked as Found.")

    @admin.action(description="Mark selected items as Not Found ❌")
    def mark_as_unfound(self, request, queryset):
        updated = queryset.update(post_status=False)
        self.message_user(request, f"{updated} item(s) marked as Not Found.")