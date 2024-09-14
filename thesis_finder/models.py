from django.db import models
from django.contrib.auth.models import User


class ThesisMemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    university_id = models.CharField(max_length=50, unique=True)
    skills = models.TextField()
    research_interests = models.TextField()
    thesis_supervisor = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    availability = models.BooleanField(default=True)
    contact_info = models.CharField(max_length=15, blank=True, null=True)
    thesis_topic = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True)

    class Meta:
        db_table = 'thesis_member_profiles'

    def __str__(self):
        return self.user.username
