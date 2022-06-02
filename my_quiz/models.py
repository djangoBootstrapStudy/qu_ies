from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자의 계정이 삭제되면 퀴즈도 삭제됨
    title = models.CharField(max_length=50) # 최대 길이 50

    class Meta:
        verbose_name_plural = 'Quizzes' # 정확한 복수으로 수정