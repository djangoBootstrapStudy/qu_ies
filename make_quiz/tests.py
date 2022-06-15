from django.test import TestCase,Client
from django.contrib.auth.models import User
from my_quiz.models import Quiz

# Create your tests here.
#create_quiz test
class TestView(TestCase):
    #SetUP
    def setUp(self):
        self.client=Client()
        #사용자
        User.objects.create_user('mj','password')

    #로그인여부 확인
    def test_check_login(self):
        #When
        login=self.client.login(username='mj',password='password')
        #Then
        self.assertFalse(login) #아직 로그인 구현 안함

    #퀴즈생성 페이지 이동
    def test_create_quiz_page(self):
        #Given
        response=self.client.get('/you-qui-es/')
        #Then
        self.assertEqual(response.status_code,200)

    #퀴즈1개 제대로 생성되었는지 확인
    def test_create_quiz(self):
        #Given
        user=User.objects.get(username='mj')
        #When
        quiz_001=Quiz.objects.create(
            author=user,
            title="mj의 quiz입니다."
        )
        #Then
        self.assertEqual(Quiz.objects.count(),1)

    #퀴즈생성후 문제, 보기 생성 확인
    #테스트제목 확인
