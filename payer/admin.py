from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import Event, Payment


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_fee_amount(self):
        fee = self.cleaned_data['fee_amount']
        if fee < 0:
            raise forms.ValidationError("Fee must be positive.")
        return fee


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('name', 'date', 'fee_amount', 'image_tag', 'created_at')
    readonly_fields = ('image_tag', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('date',)
    ordering = ('-date',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        return "-"

    image_tag.short_description = 'Event Image'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'event')
    search_fields = ('student__username', 'transaction_id', 'event__name')
    readonly_fields = ('created_at',)
