from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import ResearchPaper, Author

admin.site.register(ResearchPaper)
admin.site.register(Author)