from django.urls import path

from . import views

urlpatterns = [
    path("you-qui-es/", views.create),
    path(
        "done-qui-es/",
        views.done,
    ),
]
