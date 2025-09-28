# apps/research/serializers.py
from rest_framework import serializers
from .models import ResearchPaper

class ResearchPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchPaper
        fields = [
            'id',           # UUID primary key
            'title',
            'abstract',
            'field',
            'research_pdf',
            'author',
            'publication_date',
            'rating',
            'citations',
        ]
