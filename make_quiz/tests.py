from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase

from my_quiz.models import Quiz

from .models import QuizExample, QuizQuestion
from .views import create_question, create_quiz


# Create your tests here.
# create_quiz test
class TestView(TestCase):
    # SetUP
    def setUp(self):
        self.client = Client()
        # 사용자
        self.user = User.objects.create_user("mj", "password")

    # 로그인여부 확인
    def test_check_login(self):
        # When
        login = self.client.login(username="mj", password="password")
        # Then
        self.assertFalse(login)  # 아직 로그인 구현 안함

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

        # 문제 하나에 보기 4개 생성

        #
        # def test_create_quiz(self):
        #     #given
        #     data={
        #         'author':self.user
        #         'title':"test게시물입니다.",
        #     }
        #     #when
        #     self.client.post('/you-qui-es/',data)
        #     print("1")
        #
        #     #Then
        #     self.assertEqual(Quiz.objects.get(id=1).title, "test게시물입니다.")
        #
        #
        # def test_create_all_quiz(self):
        #     # Given
        #     user = User.objects.get(username='mj')
        #     quiz_001 = Quiz.objects.create(
        #         author=user,
        #         title="mj의 quiz입니다."
        #     )
        #     # When
        #     quesion_001 = QuizQuestion.objects.create(
        #         quiz=quiz_001,
        #         no=1,  # html만들면 변경
        #         content="내가 좋아하는 계절은?",
        #         answer=1,  # html만들면 변경
        #     )
        #     example_001 = QuizExample.objects.create(
        #         question=quesion_001,
        #         no=1,
        #         content="봄",
        #     )
        #     example_002 = QuizExample.objects.create(
        #         question=quesion_001,
        #         no=2,
        #         content="여름",
        #     )
        #     example_003 = QuizExample.objects.create(
        #         question=quesion_001,
        #         no=3,
        #         content="가을",
        #     )
        #     example_004 = QuizExample.objects.create(
        #         question=quesion_001,
        #         no=4,
        #         content="겨울",
        #     )
        #     # Then
        #
        #     # 퀴즈의 문제가 10개 이하인지 확인
        #     self.assertEqual(QuizQuestion.objects.count(), 1)
        #     # 보기가 4개인지 확인

        # 퀴즈생성후 문제, 보기 생성 확인
        # 테스트제목 확인
