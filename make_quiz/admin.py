from django.contrib import admin
from .models import QuizQuestion,QuizExample
# Register your models here.

admin.site.register(QuizQuestion)
admin.site.register(QuizExample)