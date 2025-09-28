# apps/research/urls.py
from django.urls import path
from .views import ResearchPaperListAPI, ResearchPaperDetailAPI

urlpatterns = [
    path('', ResearchPaperListAPI.as_view(), name='api_research_list'),        # list & create
    path('<uuid:pk>', ResearchPaperDetailAPI.as_view(), name='api_research_detail'),  # retrieve, update, delete
]
