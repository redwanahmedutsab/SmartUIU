from django.contrib import admin
from .models import CourseDepartment, CourseMaterial, MaterialFile


# Inline for adding multiple files directly in CourseMaterial
class MaterialFileInline(admin.TabularInline):
    model = MaterialFile
    extra = 1  # Number of extra blank fields to show
    readonly_fields = ('created_at',)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'degree', 'course_code', 'material_type', 'trimester', 'user', 'created_at')
    list_filter = ('degree', 'material_type', 'trimester')  # Admin can filter by trimester
    search_fields = ('course_title', 'course_code', 'material_description', 'degree', 'trimester')
    inlines = [MaterialFileInline]


@admin.register(CourseDepartment)
class CourseDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'trimester', 'slug')
    list_filter = ('department', 'trimester')  # Admin can filter by trimester
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'department', 'trimester')
