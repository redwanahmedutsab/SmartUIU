from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Faculty Profile (Manual Info + optional image)
# -----------------------------
class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="faculty_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to="faculty_images/", blank=True, null=True)  # Optional

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.department})"


# -----------------------------
# Faculty Availability (Time Ranges for Each Day)
# -----------------------------
class FacultyAvailability(models.Model):
    DAY_CHOICES = [
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name="availabilities")
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()  # Range start
    end_time = models.TimeField()  # Range end
    duration_minutes = models.PositiveIntegerField(default=15)  # Duration of each appointment
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.faculty.first_name} {self.faculty.last_name} - {self.day_of_week} {self.start_time}-{self.end_time}"


# -----------------------------
# Appointment Booked by Student
# -----------------------------
class Appointment(models.Model):
    availability = models.ForeignKey(FacultyAvailability, on_delete=models.CASCADE, related_name="appointments")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    start_time = models.TimeField()  # Exact start time
    end_time = models.TimeField()  # Calculated from duration
    booked_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        unique_together = ("availability", "start_time")  # Prevent double booking

    def __str__(self):
        return f"{self.availability.faculty.first_name} {self.availability.faculty.last_name} - {self.start_time}-{self.end_time} by {self.student.username}"


# -----------------------------
# Optional: Appointment Notifications
# -----------------------------
class AppointmentNotification(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="notification")
    student_notified = models.BooleanField(default=False)
    faculty_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.appointment}"
