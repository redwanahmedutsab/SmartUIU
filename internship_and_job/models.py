from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Job(models.Model):
    POST_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('intern', 'Internship'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry_level', 'Entry-Level'),
        ('mid_level', 'Mid-Level'),
        ('senior_level', 'Senior-Level'),
        ('all_levels', 'All Experience Levels'),
    ]

    WORK_ENVIRONMENT_CHOICES = [
        ('in_office', 'In-Office'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Fully Remote'),
    ]

    INDUSTRY_CHOICES = [
        ('it', 'Information Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('engineering', 'Engineering'),
        ('marketing', 'Marketing'),
        ('sales', 'Sales'),
        ('others', 'Others (Specify)'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=255)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    gender = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=timezone.now)
    education_requirements = models.CharField(max_length=255, null=True, blank=True)
    previous_experience = models.CharField(max_length=255, null=True, blank=True)
    skills_needed = models.TextField(null=True, blank=True)
    other_requirements = models.TextField(null=True, blank=True)

    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, null=True, blank=True)
    work_environment = models.CharField(max_length=20, choices=WORK_ENVIRONMENT_CHOICES, null=True, blank=True)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, null=True, blank=True)
    industry_specification = models.CharField(max_length=255, null=True, blank=True)  # For specifying "Others"

    def __str__(self):
        return self.title


class CVProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    contact_email = models.EmailField()
    address = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images/', null=True,
                                      blank=True)

    def __str__(self):
        return f"{self.user.username}'s CV Profile"


class Education(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name='educations', on_delete=models.CASCADE)
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_year = models.DateField()
    end_year = models.DateField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # CGPA field added


class Experience(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name='experiences', on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Skill(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)


class Language(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name='languages', on_delete=models.CASCADE)
    language = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=255, null=True, blank=True)  # Proficiency field added


class Award(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name='awards', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    position = models.CharField(max_length=255, null=True, blank=True)
    date_awarded = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.position}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cv_profile = models.ForeignKey(CVProfile, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cv_profile.user.username} applied to {self.job.title}"
