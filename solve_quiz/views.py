import random

from django.shortcuts import render

from my_quiz.models import Quiz


def random_saying():
    sayings = [
        "늦었다고 생각할 때가 진짜 너무 늦었다",
        "내일도 할 수 있는 일을 굳이 오늘 할 필요는 없다",
        "길이 없으면 길을 찾아라, 찾아도 없으면 길을 닦아나가라",
    ]
    return random.choice(sayings)


# Create your views here.
def solve_quiz(request, pk):
    # print(pk)
    quiz = Quiz.objects.get(id=pk)
    # print(f"퀴즈의 제목: {quiz.title}")
    # print(f"퀴즈의 출제자: {quiz.author}")
    saying = random_saying()

    return render(
        request, "solve_quiz/quiz_start.html", {"quiz": quiz, "saying": saying}
    )
