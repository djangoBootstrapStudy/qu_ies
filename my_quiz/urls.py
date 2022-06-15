from django.urls import path

from .views import MyQuizDetail, MyQuizList

urlpatterns = [
    path("", MyQuizList.as_view()),  # 도메인/my-qui-es/
    path("<int:pk>/", MyQuizDetail.as_view()),  # 도메인/my-qui-es/퀴즈pk
]
