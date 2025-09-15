from django.db import models
import uuid
from user.models import User


# Create your models here.
# book : Author M:1

class Book(models.Model):
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
        RESEARCH_PAPER = "research paper", "research_paper"
    isbn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre = models.CharField(
        max_length=50,
        choices=BookGenre.choices,
        default=BookGenre.SCIENCE
    )
    cover_image = models.ImageField(
        upload_to="book_covers/",
        blank=True,
        null=True
    )
    book_pdf = models.FileField(
        upload_to="book_pdfs/",
        blank=True,
        null=True
    )
    book_online = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=2, default=0)
    stock = models.BooleanField(default=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    update_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name

