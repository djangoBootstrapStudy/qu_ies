from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Quiz


# Create your views here.
class MyQuizList(ListView):
    model = Quiz


class MyQuizDetail(DetailView):
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(MyQuizDetail, self).get_context_data()
        context["title"] = Quiz.title
        return context
