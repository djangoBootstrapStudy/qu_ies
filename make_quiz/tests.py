from django.test import TestCase,Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from my_quiz.models import Quiz
from .models import QuizQuestion, QuizExample
from .views import create_quiz


# Create your tests here.
#create_quiz test
class TestView(TestCase):
    #SetUP
    def setUp(self):
        self.client=Client()
        #사용자
        self.user=User.objects.create_user('mj','password')

    #로그인여부 확인
    def test_check_login(self):
        #When
        login=self.client.login(username='mj',password='password')
        #Then
        self.assertFalse(login) #아직 로그인 구현 안함

    #퀴즈생성 페이지 이동
    def test_move_quiz_page(self):
        #Given
        self.client.login(username=self.user.username, password=self.user.password)
        response=self.client.get('/you-qui-es/')
        #when
        soup=BeautifulSoup(response.content,'html.parser')
        #then
        self.assertEqual(response.status_code, 203)
        self.assertEqual('퀴즈',soup.title.text)

    #퀴즈 1개 생성
    def test_create_quiz(self):
        #Given
        data={
            "title": "올바른 quiz입니다."
        }
        #when
        create_quiz(self.user,data)
        #then
        self.assertNotEqual(Quiz.objects.last().title, "잘못된 quiz입니다.") #잘못된 quiz생성
        self.assertEqual(Quiz.objects.last().title, data['title']) #quiz생성

    # 퀴즈에 문제 1개 생성
    def test_create_one_question_in_quiz(self):
        # Given
        #퀴즈 1개 생성 & 문제생성시 필요한 데이터
        self.quiz_001 = Quiz.objects.create(author=self.user, title="test퀴즈입니다.") #1
        data = {
            'quiz': self.quiz_001.id,
            'no': 1, #수정해야됨
            'content': "내가 좋아하는 계절은?",
            'answer': 1, #수정해야됨
        }
        # When
        #문제 생성함수
        create_question(self.quiz_001, data)

        # Then
        # 퀴즈가 동일한지
        # 퀴즈의 문제개수가 10개 이하인지
        # answer이 같은지
        self.assertEqual(QuizQuestion.objects.last().quiz, data['quiz'])
        self.assertTrue(QuizQuestion.objects.filter(quiz=self.quiz_001.id).count() <= 10)
        self.assertEqual(QuizQuestion.objects.get(quiz=self.quiz_001.id).answer, data['answer'])