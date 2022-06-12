from django.db import models
from my_quiz.models import Quiz

# Create your models here.
class QuizQuestion(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    no=models.IntegerField("문제번호")
    content=models.CharField(max_length=250)
    answer = models.IntegerField("문제해답")


class QuizExample(models.Model):
    question=models.ForeignKey(QuizQuestion,on_delete=models.CASCADE)
    no=models.IntegerField("보기번호")
    content=models.CharField(max_length=250)

