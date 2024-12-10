from django.contrib import admin
from .models import (
    PersonalInfo,
    WorkExperience,
    Project,
    TechnicalSkill,
    Education,
    Certification,
    Achievement,
    LanguageSkill
)

@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'years_of_experience', 'current_location', 'availability_status']
    list_filter = ['open_to_remote', 'open_to_relocation', 'availability_status']
    search_fields = ['user__username', 'user__email', 'headline', 'professional_summary']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['company', 'position', 'key_achievements']
    date_hierarchy = 'start_date'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('personal_info')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_ongoing', 'is_featured']
    list_filter = ['is_ongoing', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'problem_solved']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    list_editable = ['is_featured']

@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'years_experience', 'is_primary_skill']
    list_filter = ['category', 'is_primary_skill', 'proficiency_level']
    search_fields = ['name', 'category']
    list_editable = ['proficiency_level', 'is_primary_skill']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'degree']
    search_fields = ['institution', 'degree', 'field_of_study']
    date_hierarchy = 'start_date'

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'issue_date', 'expiry_date']
    list_filter = ['issuing_organization', 'issue_date']
    search_fields = ['name', 'issuing_organization', 'credential_id']
    date_hierarchy = 'issue_date'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date']
    list_filter = ['category', 'date']
    search_fields = ['title', 'description', 'impact']
    date_hierarchy = 'date'

@admin.register(LanguageSkill)
class LanguageSkillAdmin(admin.ModelAdmin):
    list_display = ['language', 'proficiency_level', 'certification']
    list_filter = ['proficiency_level']
    search_fields = ['language', 'certification']
    list_editable = ['proficiency_level']

# Personalización adicional del sitio admin
admin.site.site_header = "Gestión de Portafolio"
admin.site.site_title = "Panel de Administración del Portafolio"
admin.site.index_title = "Bienvenido al Panel de Gestión"