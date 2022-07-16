from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.start_quiz),
    path("<int:pk>/solving/", views.solve_quiz),
    path("<int:pk>/result/", views.result_quiz),
]
