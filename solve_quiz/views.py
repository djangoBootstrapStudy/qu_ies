from django.shortcuts import render


# Create your views here.
def solve_quiz(request, pk):
    # print(pk)
    return render(request, "solve_quiz/quiz_start.html")
