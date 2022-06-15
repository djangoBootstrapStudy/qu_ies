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
