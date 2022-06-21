from django.contrib import admin

from .models import Quiz

# Register your models here.
admin.site.register(Quiz)  # admin 페이지에 My_Quiz 섹션과 Quiz 메뉴
