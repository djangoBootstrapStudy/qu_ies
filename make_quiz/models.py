from django.db import models

from my_quiz.models import Quiz


# Create your models here.
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="퀴즈", on_delete=models.CASCADE)
    no = models.IntegerField("문제번호")
    content = models.CharField("문제내용", max_length=250)

    def __str__(self):
        return f"문제{self.no}번"


class QuizExample(models.Model):
    question = models.ForeignKey(
        QuizQuestion, verbose_name="문제", on_delete=models.CASCADE
    )
    no = models.IntegerField("보기번호")
    content = models.CharField("보기내용", max_length=250)
    answer = models.BooleanField("문제해답", default=False)

    def __str__(self):
        return f"{self.question}-보기({self.no})"
