from django import forms
from .models import CVProfile, Education, Experience, Skill, Language, Award


class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = ['bio', 'contact_email', 'contact_phone', 'profile_image']


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_year', 'end_year', 'description']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'description']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language', 'proficiency']


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'description']
