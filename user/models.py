from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        AUTHOR = 'author', 'Author'

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.USER
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

