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
    # {
    # "message": "success",
    #     }


def create(request):
    if request.method == "POST":
        user = User.objects.get(pk=1)
        title = request.POST.get("title")
        question_content = request.POST.get("question")

        data = {
            # quiz
            "title": title,
            # question
            "question_content": question_content,
        }

        quiz = create_quiz(user, data)

        try:
            no = QuizQuestion.objects.filter(quiz=quiz).count() + 1
        except:
            if no > 10:
                return render(
                    request, "make_quiz.html", {"message": "문제는 최대 10개까지만 만들수 있습니다."}
                )

        question = create_question(quiz, no, data)

        return redirect("/done-qui-es/")

    else:
        return render(request, "make_quiz.html")


def done(request):
    return render(request, "done_quiz.html")
