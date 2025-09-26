from django.contrib import admin
from .models import CourseMaterial, MaterialFile

class MaterialFileInline(admin.TabularInline):
    model = MaterialFile
    extra = 1  # Show one empty file upload form by default

@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_code', 'degree', 'trimester', 'admin_email', 'created_at')
    search_fields = ('course_title', 'course_code', 'degree')
    list_filter = ('degree', 'trimester', 'material_type')
    inlines = [MaterialFileInline]  # Allow adding files inline
