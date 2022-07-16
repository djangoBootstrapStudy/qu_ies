from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, UpdateView

from make_quiz.models import QuizExample, QuizQuestion  # UpdateView에서 필요

from .models import Quiz


# Create your views here.
class MyQuizList(ListView):
    model = Quiz
    template_name = "my_quiz/myquiz.html"

    def dispatch(self, request, *args, **kwargs):  # 비정상적인 접근 처리
        if request.user.is_authenticated:  # 로그인한 사용자의 자신의 퀴즈만 보임
            return super(MyQuizList, self).dispatch(request, *args, **kwargs)

        else:
            raise PermissionDenied


class MyQuizUpdate(UpdateView):  # TODO : 배포 후에 손대기!!!!!!
    model = Quiz
    fields = ["title", ""]  # 어떻게???

    template_name = "make_quiz.html"

    def get_context_data(self, **kwargs):
        context = super(MyQuizUpdate, self).get_context_data()
        context["title"] = Quiz.title
        context["question"] = QuizQuestion.content
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(MyQuizUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_quiz(request):
    if request.method == "POST":
        deletes = request.POST.getlist("deletes[]")
        if len(deletes) == 0:
            return redirect("/my-qui-es/")
        for i in deletes:
            delete_quiz = Quiz.objects.get(pk=i)
        if request.user.is_authenticated and request.user == delete_quiz.author:
            # 사용자가 로그인되어 있고, 퀴즈를 작성한 사람일 때 삭제 가능
            delete_quiz.delete()
        else:
            raise PermissionDenied

    return redirect("/my-qui-es/")


def main(request):
    if Quiz.objects.filter(private=False):
        # 조회수로 정렬
        hit_sort_quiz = list(Quiz.objects.order_by("-hit"))
        hit_quiz = hit_sort_quiz[:5]

        # create_at으로 정렬
        create_sort_quiz = list(Quiz.objects.order_by("-create_at"))
        current_quiz = create_sort_quiz[:5]

    if request.user.is_authenticated:
        return render(
            request, "main.html", {"hit_quiz": hit_quiz, "current_quiz": current_quiz}
        )

    if request.method == "POST":
        # 첫번째 인자로 request 를 받아야 한다.
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 유효성 검사를 통과하면 세션을 create 해야 함 -> login()
            auth_login(request, form.get_user())
            # url 에 next 가 있을 때랑 없을때 결과가 다름
            return redirect(request.GET.get("next") or "main")
    else:
        # 로그인에 필요한 빈 종이를 생성해서 lognin.html 에 전달
        form = AuthenticationForm()

    context = {
        "form": form,
        "hit_quiz": hit_quiz,
        "current_quiz": current_quiz,
    }

    return render(request, "main.html", context)
