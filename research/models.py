from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import os
from django.conf import settings

class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='research_authors')
    def __str__(self):
        return self.user.username

def validate_pdf(fieldfile_obj):
    # Ensure it's a PDF
    ext = os.path.splitext(fieldfile_obj.name)[1].lower()
    if ext != ".pdf":
        raise ValidationError("Only PDF files are allowed.")


class ResearchPaper(models.Model):
    class ResearchField(models.TextChoices):
        COMPUTER_SCIENCE = "cs", "Computer Science"
        MEDICINE = "medicine", "Medicine"
        ENGINEERING = "engineering", "Engineering"
        PHYSICS = "physics", "Physics"
        CHEMISTRY = "chemistry", "Chemistry"
        BIOLOGY = "biology", "Biology"
        ECONOMICS = "economics", "Economics"
        MATHEMATICS = "mathematics", "Mathematics"
        SOCIAL_SCIENCE = "social_science", "Social Science"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    abstract = models.TextField(max_length=2000, blank=True)
    field = models.CharField(
        max_length=50,
        choices=ResearchField.choices,
        default=ResearchField.OTHER
    )
    research_pdf = models.FileField(
        upload_to="research_papers/",
        blank=True,
        null=True,
        validators=[validate_pdf]
    )
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name="research_papers")
    publication_date = models.DateField()
    rating = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    citations = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



