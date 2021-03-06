from django.shortcuts import redirect, render

from my_quiz.models import Quiz

from .models import QuizExample, QuizQuestion


# Create your views here.
# todo: 퀴즈생성 함수
def create_quiz(user, title, private):
    quiz = Quiz.objects.create(author=user, title=title)

    if private:  # True(비공개설정)
        quiz.private = True
        quiz.save()

    return quiz


# todo: 문제생성 함수
def create_question(quiz, question_no, content):
    return QuizQuestion.objects.create(quiz=quiz, no=question_no, content=content)


# todo: 보기생성 함수
def create_example(question, data):
    QuizExample.objects.bulk_create(
        [
            QuizExample(
                question=question,
                no=data["example1"]["no"],
                content=data["example1"]["content"],
            ),
            QuizExample(
                question=question,
                no=data["example2"]["no"],
                content=data["example2"]["content"],
            ),
            QuizExample(
                question=question,
                no=data["example3"]["no"],
                content=data["example3"]["content"],
            ),
            QuizExample(
                question=question,
                no=data["example4"]["no"],
                content=data["example4"]["content"],
            ),
        ]
    )

    quizexample_answer = QuizExample.objects.get(
        question=question, no=data["answer"]["no"]
    )
    quizexample_answer.answer = True
    quizexample_answer.save()


def create_my_quiz(request):
    user = request.user
    print(user)
    if user.is_authenticated:  # 로그인하면
        if request.method == "POST":  # POST

            # todo: 퀴즈생성
            title = request.POST.get("title")
            private = request.POST.get("flexCheckDefault")
            quiz = create_quiz(user, title, private)

            for question_no in range(1, 11):

                # todo: 문제생성
                question_content = request.POST.get(f"question{question_no}")
                question = create_question(quiz, question_no, question_content)

                # todo: 보기생성
                example1 = request.POST.get(f"q{question_no}_1")
                example2 = request.POST.get(f"q{question_no}_2")
                example3 = request.POST.get(f"q{question_no}_3")
                example4 = request.POST.get(f"q{question_no}_4")
                answer = request.POST.get(f"example{question_no}")
                data = {
                    "example1": {"no": 1, "content": example1},
                    "example2": {"no": 2, "content": example2},
                    "example3": {"no": 3, "content": example3},
                    "example4": {"no": 4, "content": example4},
                    "answer": {"no": answer},
                }
                create_example(question, data)

            return redirect(f"/done-qui-es/{quiz.pk}/")

        else:  # GET
            return render(request, "make_quiz/make_quiz.html")

    else:  # 로그인하지 않으면
        return render(request, "main.html", {"messages": "로그인을 해주세요."})


def done_my_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "make_quiz/done_quiz.html", {"quiz_title": quiz.title})
