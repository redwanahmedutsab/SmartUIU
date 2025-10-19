from django.contrib import admin
from .models import Course, ClassRoutine, Note, Task, Reminder


# ----------------------------------
# Course Admin
# ----------------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'instructor', 'room')
    search_fields = ('name', 'code', 'instructor')
    list_filter = ('instructor',)
    ordering = ('name',)


# ----------------------------------
# Class Routine Admin
# ----------------------------------
@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'course_name',
        'faculty_name',
        'day_of_week',
        'start_time',
        'end_time',
        'location',
    )
    list_filter = ('day_of_week', 'faculty_name')
    search_fields = ('course_name', 'faculty_name', 'user__username')
    ordering = ('day_of_week', 'start_time')
    readonly_fields = ('created_at',)


# ----------------------------------
# Note Admin
# ----------------------------------
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'tags', 'updated_at')
    search_fields = ('title', 'tags', 'content', 'user__username')
    ordering = ('-updated_at',)
    list_filter = ('tags',)
    readonly_fields = ('updated_at',)


# ----------------------------------
# Task Admin
# ----------------------------------
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'due_date', 'completed')
    list_filter = ('completed', 'due_date')
    search_fields = ('title', 'user__username')
    ordering = ('due_date',)
    list_editable = ('completed',)
    actions = ['mark_as_completed']

    @admin.action(description="Mark selected tasks as completed")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f"{updated} task(s) marked as completed.")


# ----------------------------------
# Reminder Admin
# ----------------------------------
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'reminder_date', 'notify_days_before', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('reminder_date',)
    ordering = ('-reminder_date',)
    readonly_fields = ('created_at',)
    actions = ['mark_as_due_today']

    @admin.action(description="Set selected reminders to today")
    def mark_as_due_today(self, request, queryset):
        from django.utils import timezone
        today = timezone.now()
        updated = queryset.update(reminder_date=today)
        self.message_user(request, f"{updated} reminder(s) updated to today's date.")