from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from my_quiz.models import Quiz
from .models import QuizQuestion,QuizExample



# Create your views here.
def create_quiz(user,data):
    return Quiz.objects.create(author=user,title=data['title'])

def create_question(quiz,no,data):
    return QuizQuestion.objects.create(
        quiz=quiz,
        no=no,
        content=data['question_content'],
        answer=data['answer'],
    )
        # {
        # "message": "success",
        #     }

def create(request):
    if request.method == "POST":
        user=User.objects.get(pk=1)
        title=request.POST.get('title')
        question_content=request.POST.get('question')

        data={
            'title':title,
            'question_content':question_content,
            'answer':3,
        }

        quiz=create_quiz(user,data)

        try:
            no=QuizQuestion.objects.filter(quiz=quiz).count()+1
        except:
            if no>10:
                return render(request,'make_quiz.html',{'message':'문제는 최대 10개까지 만들수 있습니다.'})

        question=create_question(quiz,no,data)

        return redirect('/done-qui-es/')

    else:
        return render(request,'make_quiz.html')


def done(request):
    return render(request,'done_quiz.html')

