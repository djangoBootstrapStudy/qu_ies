from django.urls import path
from .views import MyQuizList

urlpatterns = [
    path('', MyQuizList.as_view()),  # 도메인/my-qui-es/
]
