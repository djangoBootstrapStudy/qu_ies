from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from django.views.generic import DetailView, ListView

from .models import Quiz


# Create your views here.
class MyQuizList(ListView):
    model = Quiz

    def dispatch(self, request, *args, **kwargs):  # 비정상적인 접근 처리
        for q in Quiz.objects.all():
            if (
                request.user.is_authenticated and request.user == q.author
            ):  # 로그인한 사용자의 자신의 퀴즈만 보임
                return super(MyQuizList, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class MyQuizDetail(DetailView):  # TODO : UpdateView로 바꾸기
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(MyQuizDetail, self).get_context_data()
        context["title"] = Quiz.title
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(MyQuizDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_quiz(request):
    if request.method == "POST":
        deletes = request.POST.getlist("deletes[]")
        for i in deletes:
            delete_quiz = Quiz.objects.get(pk=i)
        if request.user.is_authenticated and request.user == delete_quiz.author:
            # 사용자가 로그인되어 있고, 퀴즈를 작성한 사람일 때 삭제 가능
            delete_quiz.delete()
        else:
            raise PermissionDenied

    return redirect("/my-qui-es/")
