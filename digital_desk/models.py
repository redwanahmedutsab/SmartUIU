from django.db import models
from django.contrib.auth.models import User


# ----------------------------------
# Courses (optional, still used for reference)
# ----------------------------------
class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)
    instructor = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name


# ----------------------------------
# Class Routine
# ----------------------------------
class ClassRoutine(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Editable course/faculty fields
    course_name = models.CharField(max_length=255, default='Unknown Course')
    faculty_name = models.CharField(max_length=255, default='Unknown Faculty')
    # Optional FK if you want to link to a Course table
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)

    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.course_name} ({self.faculty_name}) - {self.day_of_week} ({self.start_time}-{self.end_time})"


# ----------------------------------
# Notes
# ----------------------------------
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.CharField(max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ----------------------------------
# Tasks / To-Do
# ----------------------------------
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# ----------------------------------
# Reminders
# ----------------------------------
class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    reminder_date = models.DateTimeField()
    notify_days_before = models.PositiveIntegerField(default=1)  # notify N days before
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.reminder_date})"

    @property
    def notify_date(self):
        from datetime import timedelta
        return self.reminder_date - timedelta(days=self.notify_days_before)