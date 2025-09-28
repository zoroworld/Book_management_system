from django.db import models
import uuid
from user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import os

# Create your models here.
# book : Author M:1

class Book(models.Model):
    def validate_image(fieldfile_obj):
        # Ensure it's an image
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        ext = os.path.splitext(fieldfile_obj.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError("Only image files are allowed (jpg, jpeg, png, gif, webp).")

    def validate_pdf(fieldfile_obj):
        # Ensure it's a PDF
        ext = os.path.splitext(fieldfile_obj.name)[1].lower()
        if ext != ".pdf":
            raise ValidationError("Only PDF files are allowed.")

    class BookGenre(models.TextChoices):
        FICTION = "fiction", "Fiction"
        NON_FICTION = "non_fiction", "Non-Fiction"
        STUDIES = "studies", "Studies"
        NOVEL = "novel", "Novel"
        POETRY = "poetry", "Poetry"
        DRAMA = "drama", "Drama"
        HISTORY = "history", "History"
        SCIENCE = "science", "Science"
        FANTASY = "fantasy", "Fantasy"
        MYSTERY = "mystery", "Mystery"
        BIOGRAPHY = "biography", "Biography"
        COMICS = "comics", "Comics"
        CHILDREN = "children", "Children"
        RELIGION = "religion", "Religion"
        PHILOSOPHY = "philosophy", "Philosophy"
        ROMANCE = "romance", "Romance"
        HORROR = "horror", "Horror"
    isbn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre = models.CharField(
        max_length=50,
        choices=BookGenre.choices,
        default=BookGenre.SCIENCE
    )
    cover_image = models.ImageField(
        upload_to="book_covers/",
        blank=True,
        null=True,
        validators=[validate_image]
    )
    book_pdf = models.FileField(
        upload_to="book_pdfs/",
        blank=True,
        null=True,
        validators=[validate_pdf]
    )
    book_online = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    stock = models.BooleanField(default=True)
    total_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def is_in_stock(self):
        return self.total_stock > 0


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='book_authors')
    def __str__(self):
        return self.user.name

