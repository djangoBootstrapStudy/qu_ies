from django.shortcuts import render

from my_quiz.models import Quiz


# Create your views here.
def solve_quiz(request, pk):
    # print(pk)
    quiz = Quiz.objects.get(id=pk)
    # print(f"퀴즈의 제목: {quiz.title}")
    # print(f"퀴즈의 출제자: {quiz.author}")

    return render(request, "solve_quiz/quiz_start.html", {"quiz": quiz})
