from django.contrib import admin
from .models import Product, ProductImage, Tag


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'caption')
    readonly_fields = ()
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'seller', 'category', 'price', 'availability',
        'condition', 'location', 'date_listed'
    )
    list_filter = (
        'category', 'availability', 'condition', 'date_listed', 'location'
    )
    search_fields = (
        'name', 'description', 'seller__username', 'category', 'location', 'tags__name'
    )
    readonly_fields = ('date_listed',)
    ordering = ('-date_listed',)
    list_per_page = 20
    autocomplete_fields = ['seller', 'tags']
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'price', 'category', 'condition', 'availability')
        }),
        ('Seller Info', {
            'fields': ('seller', 'phone', 'location')
        }),
        ('Additional Details', {
            'fields': ('shipping_details', 'tags')
        }),
        ('Timestamps', {
            'fields': ('date_listed',)
        }),
    )

    actions = ['mark_available', 'mark_unavailable']

    @admin.action(description="Mark selected products as Available ✅")
    def mark_available(self, request, queryset):
        updated = queryset.update(availability=True)
        self.message_user(request, f"{updated} product(s) marked as available.")

    @admin.action(description="Mark selected products as Unavailable ❌")
    def mark_unavailable(self, request, queryset):
        updated = queryset.update(availability=False)
        self.message_user(request, f"{updated} product(s) marked as unavailable.")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    ordering = ('name',)