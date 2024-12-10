from django.urls import path
from .views import LandingPageView, ProjectDetailView, ExperienceDetailView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('project/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('experience/<int:pk>/', ExperienceDetailView.as_view(), name='experience_detail'),
]