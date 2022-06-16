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

        self.quiz_002 = Quiz.objects.create(
            author=self.user_mango, title="애플망고 vs 망고스틴"
        )

        self.my_quiz_url = "/my-qui-es/"  # My Quiz 페이지 url
        self.quiz_001_url = f"/my-qui-es/{self.quiz_001.pk}"  # 퀴즈 001의 디테일 페이지 url

    # TODO : Given-When-Then 으로 작성!!

    def test_enter_my_quiz(self):
        """제대로 로그인 한 경우 /my-qui-es/ 접속 가능 -> status code는 200"""
        # Given
        self.client.login(username=self.user_mango.username, password="lovemango")
        # When
        response = self.client.get(self.my_quiz_url)
        # Then
        self.assertEqual(response.status_code, 200)

    def test_reject_my_quiz(self):
        """잘못된 로그인 시도했을 때 /my-qui-es/ 접속 불가능 -> status code가 200이면 안됨"""
        # Given
        self.client.login(
            username=self.user_mango.username, password="hatemango"
        )  # 존재하지 않는 유저 로그인 시도
        # When
        response = self.client.get(self.my_quiz_url)
        # Then
        self.assertNotEqual(response.status_code, 200)

    def test_logout(self):
        """로그아웃 했을 때는 /my-qui-es/ 접속 불가능 -> status code가 200이면 안됨"""
        # Given
        self.client.logout()
        # When
        response = self.client.get(self.my_quiz_url)
        # Then
        self.assertNotEqual(response.status_code, 200)

    def test_quiz_list(self):
        """로그인 한 후 정상적으로 /my-qui-es/ 접속 -> 로그인한 사용자의 퀴즈만 존재하는지 테스트"""
        # Given
        self.client.login(username=self.user_mango.username, password="lovemango")

        # When
        response = self.client.get(self.my_quiz_url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")  # quiz 리스트가 있는 영역
        count_quiz = len(main_area.find_all("li"))

        # Then
        # 페이지에서 보이는 퀴즈의 개수와 로그인한 사용자가 만든 퀴즈의 개수 비교
        self.assertEqual(count_quiz, len(Quiz.objects.filter(author=self.user_mango)))
        # 로그인한 사용자의 퀴즈만 존재하는지 확인
        for q in Quiz.objects.filter(author=self.user_mango):
            quiz_title = main_area.find("a", id=f"quiz-{q.pk}")
            self.assertEqual(quiz_title.text, q.title)

        # '메인으로' 버튼 유무
        self.assertTrue(main_area.find("a", id="goto-main"))

    def test_delete_quiz(self):
        """로그인한 사용자가 삭제할 퀴즈를 체크박스로 선택 -> 삭제 버튼을 눌러 삭제하는 과정을 테스트"""
        # Given
        self.client.login(username=self.user_mango.username, password="lovemango")

        # Then
        response = self.client.get(self.my_quiz_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")  # quiz 리스트가 있는 영역

        # check box 클릭 -> 삭제
        checkbox = main_area.find("input", type="checkbox")
        self.assertEqual(checkbox.attrs["name"], "deletes[]")
        checkbox.attrs[
            "name"
        ] = f"delete['{self.quiz_001.pk}','{self.quiz_002.pk}']"  # quiz_001과 quiz_002의 체크박스 선택
        if checkbox.attrs["name"] == "delete['1', '2']":
            self.quiz_001.delete()
            self.quiz_002.delete()

        # Then
        self.assertNotIn(main_area.text, self.quiz_001.title)  # quiz_001의 제목이 존재하지 않음
        self.assertNotIn(main_area.text, self.quiz_002.title)  # quiz_002의 제목이 존재하지 않음

    # TODO : Update 페이지 테스트
