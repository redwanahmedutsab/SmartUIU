from django.contrib import admin
from .models import Event, EventRegistration


# ----------------------------------
# Inline: Registrations inside Event
# ----------------------------------
class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0  # No extra blank forms by default
    readonly_fields = ('user', 'registered_at')
    can_delete = True
    ordering = ('-registered_at',)


# ----------------------------------
# Event Admin
# ----------------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date', 'time', 'location', 'created_by')
    list_filter = ('club', 'date')
    search_fields = ('title', 'description', 'location', 'club', 'created_by__username')
    ordering = ('-date', '-time')
    prepopulated_fields = {'slug': ('title',)}  # Auto-slugify in admin too
    readonly_fields = ('slug',)
    inlines = [EventRegistrationInline]

    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'banner', 'slug')
        }),
        ('Schedule & Location', {
            'fields': ('date', 'time', 'location', 'club')
        }),
        ('Organizer', {
            'fields': ('created_by',)
        }),
    )


# ----------------------------------
# Event Registration Admin
# ----------------------------------
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at')
    list_filter = ('event__club', 'registered_at')
    search_fields = ('event__title', 'user__username')
    ordering = ('-registered_at',)
    readonly_fields = ('registered_at',)
    autocomplete_fields = ('event', 'user')