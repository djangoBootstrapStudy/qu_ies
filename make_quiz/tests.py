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
        self.user = User.objects.create_user("mj", "password")

    # 로그인여부 확인
    # def test_check_login(self):
    #     # When
    #     login = self.client.login(username="mj", password="password")
    #     # Then
    #     self.assertFalse(login)  # 아직 로그인 구현 안함

    # 퀴즈생성 페이지 이동
    def test_move_quiz_page(self):
        # Given
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get("/you-qui-es/")
        # when
        soup = BeautifulSoup(response.content, "html.parser")
        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual("퀴즈", soup.title.text)

    # 퀴즈 1개 생성
    def test_create_quiz(self):
        # Given
        data = {"title": "올바른 quiz입니다."}
        # when
        create_quiz(self.user, data)
        # then
        self.assertNotEqual(Quiz.objects.last().title, "잘못된 quiz입니다.")  # 잘못된 quiz생성
        self.assertEqual(Quiz.objects.last().title, data["title"])  # quiz생성

    # 퀴즈에 문제 1개 생성
    def test_create_one_question_in_quiz(self):
        # Given
        # 퀴즈 1개 생성 & 문제생성시 필요한 데이터
        self.quiz_001 = Quiz.objects.create(author=self.user, title="test퀴즈입니다.")  # 1
        self.question_no_001 = (
            QuizQuestion.objects.filter(quiz=self.quiz_001).count() + 1
        )

        data = {
            "question_content": "내가 좋아하는 계절은?",
        }
        # When
        # 문제 생성함수
        create_question(self.quiz_001, self.question_no_001, data)

        # Then
        """
        1. 문제가 생성되었는지
        2. 퀴즈가 동일한지
        3. 퀴즈의 문제개수가 10개 이하인지
        """
        # self.assertEqual(success['message'],"success")
        self.assertEqual(QuizQuestion.objects.last().quiz, self.quiz_001)
        self.assertTrue(QuizQuestion.objects.filter(quiz=self.quiz_001).count() <= 10)

    # 문제 하나에 보기 4개 생성후 개수 확인
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
        # 보기 생성시 필요한 데이터
        data = {
            "example1": "봄",
            "example2": "여름",
            "example3": "가을",
            "example4": "겨울",
        }

        # When
        # 문제의 보기 4개 생성
        for i in range(4):
            # 보기번호
            self.example_no = (
                QuizExample.objects.filter(question=self.question_001).count() + 1
            )
            # 보기생성함수
            create_example(self.question_001, self.example_no, data)

        # Then
        # 퀴즈의 문제가 1개인지 확인
        # 보기가 4개인지 확인
        # 마지막으로 만들어진 보기의 번호가 4번인지
        # 보기 4개중 answer=True인 값이 1개인지 확인
        self.assertEqual(QuizQuestion.objects.filter(quiz=self.quiz_001).count(), 1)
        self.assertEqual(
            QuizExample.objects.filter(question=self.question_001).count(), 4
        )
        self.assertEqual(
            QuizExample.objects.filter(question=self.question_001).last().no, 4
        )
        # self.assertEqual(QuizExample.objects.filter(question=self.question_001,answer=True),1)

    # 문제 하나에 퀴즈 4개의 내용 맞는지 확인 & 정답확인(나중에)
    def test_check_four_examples_contents_in_one_question_in_quiz(self):
        # Given
        self.quiz_001 = Quiz.objects.create(author=self.user, title="test퀴즈입니다.")
        self.question_no_001 = (
            QuizQuestion.objects.filter(quiz=self.quiz_001).count() + 1
        )
        self.question_001 = QuizQuestion.objects.create(
            quiz=self.quiz_001,
            no=self.question_no_001,
            content="내가 좋아하는 계절은?",
        )
        # 보기 생성시 필요한 데이터
        data = {
            "example1": "봄",
            "example2": "여름",
            "example3": "가을",
            "example4": "겨울",
        }

        # When
        # 문제의 보기 4개 생성
        for i in range(4):
            # 보기번호
            self.example_no = (
                QuizExample.objects.filter(question=self.question_001).count() + 1
            )
            # 보기생성함수
            create_example(self.question_001, self.example_no, data)

        # Then
        # 4개 보기의 값이 맞는지 확인
        self.assertEqual(
            QuizExample.objects.get(question=self.question_001, no=1).content,
            data["example1"],
        )
        self.assertEqual(
            QuizExample.objects.get(question=self.question_001, no=2).content,
            data["example2"],
        )
        self.assertEqual(
            QuizExample.objects.get(question=self.question_001, no=3).content,
            data["example3"],
        )
        self.assertEqual(
            QuizExample.objects.get(question=self.question_001, no=4).content,
            data["example4"],
        )

    # 테스트제목 확인
