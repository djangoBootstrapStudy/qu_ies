from django.contrib import admin

from .models import QuizExample, QuizQuestion

# Register your models here.

admin.site.register(QuizQuestion)
admin.site.register(QuizExample)
