from django.urls import path

from .views import MyQuizDetail, MyQuizList, delete_quiz

urlpatterns = [
    path("", MyQuizList.as_view()),  # 도메인/my-qui-es/
    path("delete/", delete_quiz, name="delete"),  # 도메인/my-qui-es/delete/
    path("<int:pk>/", MyQuizDetail.as_view()),  # 도메인/my-qui-es/퀴즈pk/
]
