from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from my_quiz.models import Quiz

from .models import QuizExample, QuizQuestion


# Create your views here.
def create_quiz(user, data):
    return Quiz.objects.create(author=user, title=data["title"])


def create_question(quiz, no, data):
    return QuizQuestion.objects.create(
        quiz=quiz,
        no=no,
        content=data["question_content"],
    )


def create_example(question, no, data):
    QuizExample.objects.create(
        question=question,
        no=no,
        content=data[f"example{no}"],
    )
    return


def create(request):
    if request.method == "POST":
        user = request.user
        if user.is_authenticated: # 로그인하면
            title = request.POST.get("title")
            question_content = request.POST.get("question")
            example1 = request.POST.get("example1")
            example2 = request.POST.get("example2")
            example3 = request.POST.get("example3")
            example4 = request.POST.get("example4")

            data = {
                # quiz
                "title": title,
                # question
                "question_content": question_content,
                # example
                "example1": example1,
                "example2": example2,
                "example3": example3,
                "example4": example4,
            }

            # 퀴즈
            quiz = create_quiz(user, data)

            # 문제
            qustion_no = QuizQuestion.objects.filter(quiz=quiz).count() + 1
            question = create_question(quiz, qustion_no, data)

            # 보기4개
            for i in range(4):
                example_no = QuizExample.objects.filter(question=question).count() + 1
                create_example(question, example_no, data)

            return redirect("/done-qui-es/") #여기서 return 이면 test가 달라짐
        else:
            return render(request, "make_quiz.html",{"message": "로그인을 해주세요"})

    else:
        return render(request, "make_quiz.html")


def done(request):
    return render(request, "done_quiz.html")
