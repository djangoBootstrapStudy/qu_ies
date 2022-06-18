from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자의 계정이 삭제되면 퀴즈도 삭제됨
    title = models.CharField(max_length=50)  # 최대 길이 50
    hit = models.PositiveIntegerField(default=0)  # 조회 수

    private = models.BooleanField(null=True)  # 체크를 안하면 Public, 체크하면 Private

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    @property
    def update_counter(self):
        """조회 수 카운트 -> 퀴즈를 클릭하면 hit에 +1"""
        self.hit = self.hit + 1
        self.save()
        return self.hit

    # TODO : get_absolute_url 정의하기
    def get_absolute_url(self):
        """모델의 레코드 URL 생성 규칙을 정의함"""
        return f"/my-qui-es/{self.pk}/"

    class Meta:
        verbose_name_plural = "Quizzes"  # 정확한 복수으로 수정
