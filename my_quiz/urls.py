from django.urls import path

from .views import MyQuizList, delete_quiz  # TODO: MyQuizUpdate 추가

urlpatterns = [
    path("", MyQuizList.as_view()),  # 도메인/my-qui-es/
    path("delete/", delete_quiz, name="delete"),  # 도메인/my-qui-es/delete/
    # TODO: Update 부분 만들 때 살리기
    # path("update/<int:pk>/", MyQuizUpdate.as_view()),  # 도메인/my-qui-es/퀴즈pk/
]
