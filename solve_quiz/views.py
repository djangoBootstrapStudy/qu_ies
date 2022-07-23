import random

from django.shortcuts import redirect, render

from make_quiz.models import QuizExample, QuizQuestion
from my_quiz.models import Quiz


def random_saying():
    sayings = [
        "늦었다고 생각할 때가 진짜 너무 늦었다",
        "내일도 할 수 있는 일을 굳이 오늘 할 필요는 없다",
        "길이 없으면 길을 찾아라, 찾아도 없으면 길을 닦아나가라",
        "부지런함을 대신할 지름길은 없다",
        "관찰만으로도 많은 것을 배울수 있다",
        "오늘 걷지 않으면 내일은 뛰어야 한다",
        "날마다 새로우며 깊어지고 넓어진다",
        "그대만큼 사랑스러운 사람을 본 일이 없다",
    ]
    return random.choice(sayings)


# Create your views here.
def start_quiz(request, pk):
    if request.method == "GET":  # get일경우
        quiz = Quiz.objects.get(id=pk)
        saying = random_saying()

        return render(
            request, "solve_quiz/quiz_start.html", {"quiz": quiz, "saying": saying}
        )
    else:  # post일경우
        """saying: 제시된 랜덤필적확인란, follow_saying: 받아쓴 필적확인란"""
        saying = request.POST["saying"]
        follow_saying = request.POST["follow-saying"]
        print(pk)
        # Todo: 필적확인란이 일치하면 세션 저장 후 quiz페이지
        if follow_saying == saying:

            tester_name = request.POST["tester-name"]
            test_date = request.POST["test-date"]

            """세션을 이용해 응시자 정보 저장"""
            request.session["tester_name"] = tester_name
            request.session["test_date"] = test_date

            return redirect(f"/qui-es/{pk}/solving/")
        # Todo:필적확인란 불일치하면 quiz_start 페이지 redirect
        else:
            return redirect(f"/qui-es/{pk}/")


def solve_quiz(request, pk):
    tester_name = request.session["tester_name"]
    if tester_name is not None:  # 세션이 있을경우
        if request.method == "GET":

            quiz = Quiz.objects.get(id=pk)

            questions = QuizQuestion.objects.filter(quiz=quiz.id)

            examples = []
            for question in questions:
                quiz_example = QuizExample.objects.filter(question=question)
                for example in quiz_example:
                    examples.append(example)

            return render(
                request,
                "solve_quiz/quiz.html",
                {"quiz": quiz, "questions": questions, "examples": examples},
            )
        else:
            answer = {}
            for question_no in range(1, 11):
                answer[question_no] = int(
                    request.POST.get(f"question{question_no}_answer")
                )
            if len(answer) == 10:
                # print(answer)
                """세션에 정답 저장"""
                request.session["answer"] = answer

                return redirect(f"/qui-es/{pk}/result/")
            else:
                return redirect(f"/qui-es/{pk}/")

    else:  # 세션이 없을경우
        return redirect(f"/qui-es/{pk}/")


def result_quiz(request, pk):
    if request.method == "GET":

        return render(request, "solve_quiz/quiz_result.html")
