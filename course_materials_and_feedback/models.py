from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class CourseMaterial(models.Model):
    degree = models.CharField(max_length=255, null=False, default='Unknown Degree')
    trimester = models.CharField(max_length=255, null=False, default='Unknown Trimester')
    course_title = models.CharField(max_length=255, null=False)
    course_code = models.CharField(max_length=255, null=False)
    material_type = models.CharField(max_length=255)
    material_description = models.TextField(blank=True, null=False)
    admin_email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(null=False, default=timezone.now().year)  # NEW
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course_title


class MaterialFile(models.Model):
    course_material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='materials/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"File for {self.course_material.course_title}"


class CourseDepartment(models.Model):
    name = models.CharField(max_length=255)  # e.g., "B.Sc. in Computer Science & Engineering"
    department = models.CharField(max_length=255)  # e.g., "Department of CSE"
    trimester = models.CharField(max_length=255, null=False, default='trimester')  # NEW
    slug = models.SlugField(unique=True, blank=True)  # e.g., "bscse"
    image = models.ImageField(upload_to='degree_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
