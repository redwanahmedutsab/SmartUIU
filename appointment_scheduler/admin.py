from django.contrib import admin
from .models import FacultyProfile, FacultyAvailability, Appointment, AppointmentNotification


# -----------------------------
# Inline: Faculty Availability inside Faculty Profile
# -----------------------------
class FacultyAvailabilityInline(admin.TabularInline):
    model = FacultyAvailability
    extra = 1  # Show one empty form for quick addition
    fields = ('day_of_week', 'start_time', 'end_time', 'duration_minutes', 'is_blocked')
    ordering = ('day_of_week', 'start_time')


# -----------------------------
# Faculty Profile Admin
# -----------------------------
@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'designation', 'user')
    search_fields = ('first_name', 'last_name', 'department', 'designation')
    list_filter = ('department',)
    inlines = [FacultyAvailabilityInline]


# -----------------------------
# Faculty Availability Admin
# -----------------------------
@admin.register(FacultyAvailability)
class FacultyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'day_of_week', 'start_time', 'end_time', 'duration_minutes', 'is_blocked')
    list_filter = ('day_of_week', 'is_blocked')
    search_fields = ('faculty__first_name', 'faculty__last_name', 'faculty__department')
    ordering = ('faculty', 'day_of_week', 'start_time')


# -----------------------------
# Appointment Admin
# -----------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('availability', 'student', 'start_time', 'end_time', 'booked_at', 'is_cancelled')
    list_filter = ('is_cancelled', 'availability__day_of_week')
    search_fields = ('student__username', 'availability__faculty__first_name', 'availability__faculty__last_name')
    ordering = ('-booked_at',)

    # Optional: make cancellation editable directly from list view
    list_editable = ('is_cancelled',)


# -----------------------------
# Appointment Notification Admin
# -----------------------------
@admin.register(AppointmentNotification)
class AppointmentNotificationAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'student_notified', 'faculty_notified', 'created_at')
    list_filter = ('student_notified', 'faculty_notified')
    search_fields = ('appointment__student__username', 'appointment__availability__faculty__first_name')
    list_editable = ('student_notified', 'faculty_notified')
