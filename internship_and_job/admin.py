from django.contrib import admin
from .models import (
    Job,
    CVProfile,
    Education,
    Experience,
    Skill,
    Language,
    Award,
    JobApplication,
)


# ----------------------------------
# Inline sections for CV Profile
# ----------------------------------
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ('degree', 'institution', 'start_year', 'end_year', 'cgpa')
    ordering = ('-start_year',)


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1
    fields = ('company', 'position', 'start_date', 'end_date')
    ordering = ('-start_date',)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('skill_name',)


class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1
    fields = ('language', 'proficiency')


class AwardInline(admin.TabularInline):
    model = Award
    extra = 1
    fields = ('title', 'position', 'date_awarded')
    ordering = ('-date_awarded',)


# ----------------------------------
# CV Profile Admin
# ----------------------------------
@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_email', 'contact_phone')
    search_fields = ('user__username', 'contact_email', 'contact_phone')
    inlines = [EducationInline, ExperienceInline, SkillInline, LanguageInline, AwardInline]
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'profile_image')
        }),
        ('Contact Details', {
            'fields': ('contact_email', 'address', 'contact_phone')
        }),
        ('Biography', {
            'fields': ('bio',)
        }),
    )


# ----------------------------------
# Job Admin
# ----------------------------------
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'company', 'post_type', 'experience_level', 'work_environment',
        'industry', 'location', 'deadline', 'posted_by'
    )
    list_filter = (
        'post_type', 'experience_level', 'work_environment', 'industry', 'deadline'
    )
    search_fields = ('title', 'company', 'location', 'posted_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'logo', 'posted_by')
        }),
        ('Job Details', {
            'fields': (
                'description', 'responsibilities', 'location',
                'post_type', 'gender', 'salary'
            )
        }),
        ('Requirements', {
            'fields': (
                'education_requirements', 'previous_experience',
                'skills_needed', 'other_requirements'
            )
        }),
        ('Experience & Environment', {
            'fields': ('experience_level', 'work_environment', 'industry', 'industry_specification')
        }),
        ('Dates', {
            'fields': ('created_at', 'deadline')
        }),
    )


# ----------------------------------
# Job Application Admin
# ----------------------------------
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'cv_profile', 'applied_at')
    list_filter = ('applied_at', 'job__industry', 'job__post_type')
    search_fields = ('job__title', 'cv_profile__user__username')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at',)
    autocomplete_fields = ('job', 'cv_profile')
    actions = ['delete_selected']

    @admin.action(description='Delete selected applications')
    def delete_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} application(s).")


# ----------------------------------
# Register supporting models separately (optional)
# ----------------------------------
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Award)