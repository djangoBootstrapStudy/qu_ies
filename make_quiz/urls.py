from django.urls import path

from . import views

urlpatterns = [
    path("you-qui-es/", views.create_my_quiz),
    path(
        "done-qui-es/",
        views.done,
    ),
    path("", views.main),
]
