from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.http import HttpResponse
import csv
from .models import Event, Payment


# ---------- Event Form ----------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean_fee_amount(self):
        fee = self.cleaned_data['fee_amount']
        if fee < 0:
            raise forms.ValidationError("Fee must be positive.")
        return fee


# ---------- Event Admin ----------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('name', 'date', 'fee_amount', 'image_tag', 'created_at', 'view_registrants_link')
    readonly_fields = ('image_tag', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('date',)
    ordering = ('-date',)
    actions = ['export_registrants_csv']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        return "-"

    image_tag.short_description = 'Event Image'

    # Link to view registered members
    def view_registrants_link(self, obj):
        return format_html('<a href="/admin/payer/payment/?event__id__exact={}">View Registrants</a>', obj.id)

    view_registrants_link.short_description = 'Registrants'

    # Action to export CSV of paid registrants
    def export_registrants_csv(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Please select exactly one event to export CSV.")
            return

        event = queryset.first()
        payments = Payment.objects.filter(event=event, status='Success')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{event.name}_registrants.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Full Name', 'Email', 'Amount Paid', 'Transaction ID', 'Date Paid'])

        for p in payments:
            writer.writerow([
                p.student.username,
                p.student.get_full_name(),
                p.student.email,
                p.amount,
                p.transaction_id,
                p.created_at.strftime("%d-%m-%Y %H:%M")
            ])
        return response

    export_registrants_csv.short_description = "Export Paid Registrants CSV"


# ---------- Payment Admin ----------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'amount', 'transaction_id', 'status', 'created_at')
    list_filter = ('status', 'event')
    search_fields = ('student__username', 'transaction_id', 'event__name')
    readonly_fields = ('created_at',)
