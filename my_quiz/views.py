from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Quiz


# Create your views here.
class MyQuizList(ListView):
    model = Quiz

