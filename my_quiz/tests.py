from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Quiz


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_mango = User.objects.create_user(
            username="mango", password="lovemango"
        )

        self.quiz_001 = Quiz.objects.create(
            author=self.user_mango,
            title="애플 망고가 되려면?",
        )

    def test_quiz_list(self):
        self.assertEqual(Quiz.objects.count(), 1)  # setup에서 생성한 퀴즈는 1개

        # 로그인 하지 않은 상태 -> 접근 불가
        response = self.client.get("/my-qui-es/")
        self.assertNotEqual(response.status_code, 200)

        # 잘못된 아이디, 패스워드로 로그인하는 경우
        self.client.login(username=self.user_mango.username, password="hatemango")
        response = self.client.get("/my-qui-es/")  # 새로고침
        self.assertNotEqual(response.status_code, 200)

        # 로그인 함 -> My Quiz 접근 가능
        self.client.login(username=self.user_mango.username, password="lovemango")
        response = self.client.get("/my-qui-es/")  # 새로고침
        self.assertEqual(response.status_code, 200)  # 로그인 했으므로 200

        # 로그인한 사용자의 퀴즈만 존재하는지 확인
        quiz_list = Quiz.objects.all()
        for quiz in quiz_list:
            self.assertEqual(quiz.author, self.user_mango)

        # html 요소 확인
        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")  # quiz 리스트가 있는 영역

        self.assertIn(
            main_area.find("a", id=f"quiz-{self.quiz_001.pk}").text, self.quiz_001.title
        )  # setUp()에서 만든 퀴즈가 존재하는지 확인

        self.assertTrue(
            main_area.find("input", id=f"checkbox-{self.quiz_001.pk}")
        )  # 삭제할 문제 선택하는 체크박스
        self.assertTrue(
            main_area.find("button", id="delete-quiz")
        )  # '삭제' 버튼 -> url & view 짜기
        self.assertTrue(main_area.find("a", id="goto-main"))  # '메인으로' 버튼

