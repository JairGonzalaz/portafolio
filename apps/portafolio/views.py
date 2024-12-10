# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404,render

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

class LandingPageView(TemplateView):
    """
    Vista principal que renderiza el landing page del portafolio.
    Recopila y organiza toda la información necesaria de los diferentes modelos.
    """
    template_name = 'portafolio/landing_page.html'

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto base de TemplateView
        context = super().get_context_data(**kwargs)
        
        # Obtenemos la información personal del usuario
        # Asumimos que solo hay un perfil personal
        try:
            personal_info = PersonalInfo.objects.select_related('user').first()
            context['personal_info'] = personal_info
            print(personal_info)
        except PersonalInfo.DoesNotExist:
            context['personal_info'] = None

        # Experiencia laboral ordenada por fecha
        context['work_experience'] = WorkExperience.objects.filter(
            personal_info=personal_info
        ).order_by('-start_date')

        # Proyectos destacados
        context['featured_projects'] = Project.objects.filter(
            personal_info=personal_info,
            is_featured=True
        ).order_by('-start_date')[:3]  # Mostramos solo los 3 más recientes

        # Habilidades técnicas agrupadas por categoría
        technical_skills = TechnicalSkill.objects.filter(
            personal_info=personal_info
        ).order_by('-is_primary_skill', 'category', '-proficiency_level')
        
        # Organizamos las habilidades en un diccionario por categoría
        skills_by_category = {}
        for skill in technical_skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        context['skills_by_category'] = skills_by_category

        # Educación
        context['education'] = Education.objects.filter(
            personal_info=personal_info
        ).order_by('-end_date')

        # Certificaciones vigentes
        context['certifications'] = Certification.objects.filter(
            personal_info=personal_info
        ).order_by('-issue_date')

        # Logros destacados
        context['achievements'] = Achievement.objects.filter(
            personal_info=personal_info
        ).order_by('-date')[:5]  # Limitamos a los 5 más recientes

        # Idiomas
        context['languages'] = LanguageSkill.objects.filter(
            personal_info=personal_info
        ).order_by('-proficiency_level')

        return context


class ProjectDetailView(DetailView):
    """
    Vista para mostrar el detalle de un proyecto específico.
    Útil cuando el usuario quiere ver más información sobre un proyecto.
    """
    model = Project
    template_name = 'portafolio/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Añadimos las tecnologías utilizadas en el proyecto
        project = self.get_object()
        context['technical_skills'] = TechnicalSkill.objects.filter(
            personal_info=project.personal_info
        )
        
        # Podríamos añadir proyectos relacionados basados en tecnologías similares
        context['related_projects'] = Project.objects.filter(
            personal_info=project.personal_info
        ).exclude(id=project.id)[:3]
        
        return context


class ExperienceDetailView(DetailView):
    """
    Vista para mostrar el detalle de una experiencia laboral específica.
    Útil para mostrar más información sobre un trabajo en particular.
    """
    model = WorkExperience
    template_name = 'portafolio/experience_detail.html'
    context_object_name = 'experience'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        experience = self.get_object()
        
        # Añadimos proyectos relacionados con esta experiencia
        context['related_projects'] = Project.objects.filter(
            personal_info=experience.personal_info,
            start_date__gte=experience.start_date,
            start_date__lte=experience.end_date or experience.start_date
        )
        
        return context