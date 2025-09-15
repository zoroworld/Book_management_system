from django.db import models

# Create your models here.
class User(models.Model):
    class UserType(models.TextChoices):
        USER = 'user'
        ADMIN = 'admin'
        AUTHOR = 'author'
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.USER
    )
    update_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(null=True, blank=True)
