from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from my_quiz.models import Quiz
from .models import QuizQuestion,QuizExample



# Create your views here.
def create_quiz(user,data):
    return Quiz.objects.create(author=user,title=data['title'])

def create(request):
    if request.method == "POST":
        user=User.objects.get(pk=1)
        title=request.POST.get('title')
        data={
            'title':title,
        }
        quiz=create_quiz(user,data)

        return redirect('/done-qui-es/')

    else:
        return render(request,'make_quiz.html')


def done(request):
    return render(request,'done_quiz.html')

