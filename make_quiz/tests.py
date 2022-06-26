from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase

from my_quiz.models import Quiz

from .models import QuizExample, QuizQuestion
from .views import create_example, create_question, create_quiz


# Create your tests here.
# create_quiz test
class TestView(TestCase):
    # SetUP
    def setUp(self):
        self.client = Client()
        # 사용자
        self.user = User.objects.create_user(username="mj", password="my_password")

    # TODO:로그인여부 확인
    # 퀴즈생성 페이지 이동시 로그인 하지 않은 사용자는 메인 페이지로 이동
    def test_not_logged_user_enter_main_page(self):
        # Given
        response = self.client.get("/you-qui-es/")
        # when
        soup = BeautifulSoup(response.content, "html.parser")
        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual("메인", soup.title.text)

    # 로그인되었을경우
    def test_check_login(self):
        # When
        login = self.client.login(username="mj", password="my_password")
        # Then
        self.assertTrue(login)

    # 퀴즈생성 페이지 이동시 로그인 한 사용자는 퀴즈생성 페이지로 정상적으로 이동
    def test_logged_user_enter_quiz_page(self):
        # Given
        self.client.login(username="mj", password="my_password")
        response = self.client.get("/you-qui-es/")
        # when
        soup = BeautifulSoup(response.content, "html.parser")
        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual("퀴즈만들기", soup.title.text)

    # todo: 퀴즈 생성 & 비공개여부
    # 퀴즈 1개 생성-공개일경우
    def test_create_quiz_public(self):
        # Given
        title = "mj의 퀴즈퀴즈퀴즈~!!! 나를 맞춰봐"
        private = False

        # when
        create_quiz(self.user, title, private)

        # then
        self.assertEqual(Quiz.objects.last().title, title)  # quiz 생성
        self.assertEqual(Quiz.objects.last().private, private)  # 공개 확인

    # 퀴즈 1개 생성-비공개일경우
    def test_create_quiz_private(self):
        # Given
        title = "mj의 퀴즈퀴즈퀴즈~!!! 나를 맞춰봐"
        private = True

        # when
        create_quiz(self.user, title, private)

        # then
        self.assertEqual(Quiz.objects.last().title, title)  # quiz 생성
        self.assertEqual(Quiz.objects.last().private, private)  # 공개 확인

    # todo: 퀴즈에 문제 1개 생성
    def test_create_one_question_in_quiz(self):
        # Given
        # 퀴즈 1개 생성 & 문제생성시 필요한 데이터
        self.quiz_001 = Quiz.objects.create(author=self.user, title="test퀴즈입니다.")  # 1
        self.question_no_001 = (
            QuizQuestion.objects.filter(quiz=self.quiz_001).count() + 1
        )
        # 문제내용
        content = "내가 좋아하는 계절은?"

        # When
        # 문제 생성함수
        create_question(self.quiz_001, self.question_no_001, content)

        # Then
        """
        1. 퀴즈가 동일한지
        2. 퀴즈의 번호가 동일한지
        3. 퀴즈의 번호가 1번인지
        4. 퀴즈의 내용이 동일한지
        """
        self.assertEqual(QuizQuestion.objects.last().quiz, self.quiz_001)
        self.assertEqual(QuizQuestion.objects.last().no, self.question_no_001)
        self.assertTrue(QuizQuestion.objects.last().no == 1)
        self.assertEqual(QuizQuestion.objects.last().content, content)

    # todo: 문제하나에 보기 4개 생성 & 답확인
    def test_create_four_examples_in_one_question_in_quiz(self):
        # Given
        # 퀴즈생성 & 퀴즈의 문제 생성
        self.quiz_001 = Quiz.objects.create(author=self.user, title="test퀴즈입니다.")
        self.question_no_001 = (
            QuizQuestion.objects.filter(quiz=self.quiz_001).count() + 1
        )
        self.question_001 = QuizQuestion.objects.create(
            quiz=self.quiz_001,
            no=self.question_no_001,
            content="내가 좋아하는 계절은?",
        )
        answer = 1
        # 보기 생성시 필요한 데이터
        data = {
            "example1": {"no": 1, "content": "봄"},
            "example2": {"no": 2, "content": "여름"},
            "example3": {"no": 3, "content": "가을"},
            "example4": {"no": 4, "content": "겨울"},
            "answer": {"no": answer},
        }

        # When
        create_example(self.question_001, data)

        # Then
        """
        1.퀴즈의 문제가 1개인지 확인
        2.보기가 4개인지 확인
        3.보기 4개중 answer=True인 값이 1개인지 확인
        4.답이 맞는지 확인
        """
        self.assertEqual(QuizQuestion.objects.filter(quiz=self.quiz_001).count(), 1)
        self.assertEqual(
            QuizExample.objects.filter(question=self.question_001).count(), 4
        )
        self.assertEqual(
            QuizExample.objects.filter(question=self.question_001, answer=True).count(),
            1,
        )
        self.assertEqual(
            QuizExample.objects.get(question=self.question_001, answer=True).no, answer
        )

    # 테스트제목 확인
