#apps/portafolio
"""aplicacion web, registrar todo acerca de mi, nombre, titulo pasatiempos, todo lo necesario para genera un CV """
from django.db import models
#____________________________________________________________
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils.text import slugify
#__________________________________________________________

class PersonalInfo(models.Model):
    """Información personal y profesional básica"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200, help_text="Un título breve que te describe profesionalmente")
    professional_summary = models.TextField(help_text="Resumen conciso de tu perfil profesional")
    years_of_experience = models.PositiveIntegerField(default=0)#calculo automatico empesando desde mayo del 2023
    current_location = models.CharField(max_length=100)
    open_to_remote = models.BooleanField(default=True)
    open_to_relocation = models.BooleanField(default=False)
    preferred_work_environment = models.TextField(help_text="Describe tu ambiente de trabajo ideal")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_website = models.URLField(blank=True)
    
    image = models.ImageField(upload_to='photos/', blank=True)
    availability_status = models.CharField(
        max_length=50,
        choices=[
            ('AVAILABLE', 'Disponible inmediatamente'),
            ('NOTICE_PERIOD', 'Disponible con previo aviso'),
            ('NOT_AVAILABLE', 'No disponible actualmente'),
        ],
        default='AVAILABLE'
    )
    notice_period = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Tiempo necesario para comenzar un nuevo proyecto"
    )
    
    class Meta:
        verbose_name_plural = "Personal Info"

class WorkExperience(models.Model):
    """Experiencia laboral detallada"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    image = models.ImageField(upload_to='imgs-company/', blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    company_description = models.TextField(help_text="Breve descripción de la empresa")
    key_achievements = models.TextField(help_text="Logros principales en el puesto")
    technologies_used = models.TextField(help_text="Tecnologías y herramientas utilizadas")
    team_size = models.PositiveIntegerField(help_text="Tamaño del equipo con el que trabajaste")
    impact_metrics = models.TextField(
        help_text="Métricas cuantificables de impacto (ej: mejora de rendimiento, reducción de costos)",
        blank=True
    )

    class Meta:
        ordering = ['-start_date']

class Project(models.Model):
    """Proyectos personales o profesionales"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)#numero interno para identificar
    description = models.TextField()
    problem_solved = models.TextField(help_text="Problema específico que resuelve el proyecto")
    key_features = models.TextField(help_text="Características principales del proyecto")
    technical_challenges = models.TextField(help_text="Desafíos técnicos enfrentados y superados")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_ongoing = models.BooleanField(default=False)
    project_url = models.URLField(blank=True)
    github_repo = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='project_images/', blank=True)
    is_featured = models.BooleanField(default=False, help_text="Proyectos destacados aparecerán primero")
    development_time = models.PositiveIntegerField(
        help_text="Tiempo de desarrollo en semanas",
        validators=[MinValueValidator(1)]
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_featured', '-start_date']


class TechnicalSkill(models.Model):
    """Habilidades técnicas con nivel de experiencia"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, help_text="Ej: Lenguajes, Frameworks, Bases de datos")
    name = models.CharField(max_length=50)
    proficiency_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nivel de 1 a 5"
    )
    years_experience = models.PositiveIntegerField()
    last_used = models.DateField(help_text="Última vez que usaste esta tecnología")
    is_primary_skill = models.BooleanField(
        default=False,
        help_text="Habilidades en las que te especializas principalmente"
    )
    projects_count = models.PositiveIntegerField(
        default=0,
        help_text="Número de proyectos donde has aplicado esta habilidad"
    )

    class Meta:
        ordering = ['-is_primary_skill', '-proficiency_level']

class Education(models.Model):
    """Formación académica y certificaciones"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    relevant_coursework = models.TextField(blank=True, help_text="Cursos relevantes para tu carrera")
    achievements = models.TextField(blank=True, help_text="Logros académicos destacados")
    thesis_title = models.CharField(max_length=200, blank=True)
    thesis_description = models.TextField(blank=True)
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )

    class Meta:
        ordering = ['-end_date']
        verbose_name_plural = "Education"

class Certification(models.Model):
    """Certificaciones y cursos especializados"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    skills_gained = models.TextField(help_text="Habilidades adquiridas en esta certificación")

    class Meta:
        ordering = ['-issue_date']

class Achievement(models.Model):
    """Logros profesionales destacados"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    category = models.CharField(
        max_length=50,
        choices=[
            ('PROFESSIONAL', 'Profesional'),
            ('ACADEMIC', 'Académico'),
            ('PERSONAL', 'Personal'),
        ]
    )
    impact = models.TextField(help_text="Impacto medible del logro")
    verification_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-date']

class LanguageSkill(models.Model):
    """Habilidades lingüísticas"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('NATIVE', 'Nativo'),
            ('FLUENT', 'Fluido'),
            ('INTERMEDIATE', 'Intermedio'),
            ('BASIC', 'Básico'),
        ]
    )
    certification = models.CharField(max_length=100, blank=True)