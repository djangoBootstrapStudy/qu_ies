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

    def get_response(self, url: str) -> int:
        """url로 접속한 페이지 return"""
        response = self.client.get(url)
        return response

    def get_status_code(self, url: str) -> int:
        """페이지 로드 시 status_code를 return"""
        return self.get_response(url).status_code

    def test_quiz_list(self):
        self.assertEqual(Quiz.objects.count(), 1)  # setup에서 생성한 퀴즈는 1개

        my_quiz_list_url = f"/my-qui-es/"

        # 로그인 하지 않은 상태 -> 접근 불가
        # TODO : views에 dipatch() 만들기
        self.assertNotEqual(self.get_status_code(my_quiz_list_url), 200)

        # 잘못된 아이디, 패스워드로 로그인하는 경우
        self.client.login(username=self.user_mango.username, password="hatemango")
        self.assertNotEqual(self.get_status_code(my_quiz_list_url), 200)

        # 로그인 함 -> My Quiz 접근 가능
        self.client.login(username=self.user_mango.username, password="lovemango")
        self.assertEqual(self.get_status_code(my_quiz_list_url), 200)  # 로그인 했으므로 200

        # 로그인한 사용자의 퀴즈만 존재하는지 확인
        quiz_list = Quiz.objects.all()
        for quiz in quiz_list:
            self.assertEqual(quiz.author, self.user_mango)

        # html 요소 확인
        soup = BeautifulSoup(self.get_response(my_quiz_list_url).content, "html.parser")
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

    def test_quiz_detail(self):  # TODO : update view로 바꾼 후 추가 작성
        # 로그인 안한 경우 -> status_code가 200 이면 안됨
        # TODO : views에 dipatch() 만들기
        self.assertNotEqual(self.get_status_code(self.quiz_001.get_absolute_url()), 200)

        # 로그인 한 경우 -> status_code가 200
        self.client.login(username=self.user_mango.username, password="lovemango")
        self.assertEqual(
            self.get_status_code(self.quiz_001.get_absolute_url()), 200
        )  # 로그인 했으므로 200

        # html 요소 확인
        soup = BeautifulSoup(
            self.get_response(self.quiz_001.get_absolute_url()).content, "html.parser"
        )
        main_area = soup.find("div", id="main-area")  # quiz의 문제와 보기가 있는 영역

        self.assertIn(main_area.find("h2").text, self.quiz_001.title)  # 퀴즈의 제목 유무 확인

        # TODO : 보기의 유무 확인 -> 문제 만들기 model이 완성되면 추가

        # TODO : 수정 버튼

        # TODO : 공개/비공개 버튼 -> checkbox

    def test_quiz_delete(self):
        # TODO : url, view 만들기

        my_quiz_list_url = "/my-qui-es/"

        # user_mango 로그인
        self.client.login(username=self.user_mango.username, password="lovemango")
        self.assertEqual(self.get_status_code(my_quiz_list_url), 200)  # 로그인 했으므로 200

        # My Quiz 페이지 가져오기
        soup = BeautifulSoup(self.get_response(my_quiz_list_url).content, "html.parser")
        main_area = soup.find("div", id="main-area")  # quiz 리스트가 있는 영역

        # My Quiz 페이지에 존재하는 퀴즈 체크
        self.assertEqual(Quiz.objects.count(), 1)
        self.assertIn(
            main_area.find("a", id=f"quiz-{self.quiz_001.pk}").text, self.quiz_001.title
        )

        # check box 클릭 -> 삭제
        checkbox = main_area.find("input", id=f"checkbox-{self.quiz_001.pk}")  # 체크박스 확인
        self.assertEqual(checkbox.attrs["name"], "deletes[]")
        checkbox.attrs["name"] = f"delete['{self.quiz_001.pk}']"  # quiz_001의 체크박스 선택

        if checkbox.attrs["name"] == "delete['1']":
            self.quiz_001.delete()

        # 삭제
        self.assertNotIn(main_area.text, self.quiz_001.title)  # quiz_001의 제목이 존재하지 않음
        self.assertEqual(Quiz.objects.count(), 0)  # 퀴즈의 개수는 0개
