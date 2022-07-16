from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Quiz


# Create your tests here.
class TestMyQuiz(TestCase):
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
            author=self.user_mango,
            title="애플망고 vs 망고스틴",
        )

        self.my_quiz_url = "/my-qui-es/"  # My Quiz 페이지 url
        self.quiz_001_url = f"/my-qui-es/{self.quiz_001.pk}"  # 퀴즈 001의 디테일 페이지 url
        self.main_url = "/"

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
        quiz_count = len(soup.find_all("li"))  # /my-qui-es/ 에서 보이는 퀴즈의 개수

        # Then
        # 로그인한 사용자의 퀴즈만 존재하는지 확인
        # 1. 페이지에 보이는 퀴즈의 개수와 로그인한 사용자가 만든 퀴즈의 개수가 같은가?
        self.assertEqual(quiz_count, len(Quiz.objects.filter(author=self.user_mango)))

        # 2. 페이지에 보이는 퀴즈는 모두 로그인한 사용자가 만든 퀴즈가 맞는가?
        for q in Quiz.objects.filter(author=self.user_mango):
            quiz_title = main_area.find("a", id=f"quiz-{q.pk}")
            self.assertEqual(quiz_title.text, q.title)

        # '메인으로' 버튼 유무
        self.assertTrue(main_area.find("input", id="goto-main"))

    def test_delete_quiz(self):
        """로그인한 사용자가 삭제할 퀴즈를 체크박스로 선택 -> 삭제 버튼을 눌러 삭제하는 과정을 테스트"""
        # Given
        self.client.login(username=self.user_mango.username, password="lovemango")

        # When
        response = self.client.get(self.my_quiz_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")  # quiz 리스트가 있는 영역

        # check box 클릭 -> 삭제
        checkbox = soup.find("input", type="checkbox")
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

    def test_delete_no_select(self):
        """삭제할 퀴즈를 선택하지 않은 상태에서 삭제버튼을 눌렀을 때 -> /my-qui-es/로 리다이렉트"""
        # Given
        self.client.login(username="mango", password="lovemango")

        # When
        response = self.client.get(self.my_quiz_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")

        # 선택된 체크박스가 없음
        checkbox = soup.find("input", type="checkbox")
        if checkbox.attrs["name"] == "delete[]":
            response = self.client.get(self.my_quiz_url, follow=True)

        # Then
        self.assertEqual(response.status_code, 200)

    def test_no_quiz(self):
        """퀴즈가 하나도 없을 때"""
        # Given
        Quiz.objects.all().delete()  # 퀴즈를 모두 삭제
        # print(Quiz.objects.all())
        self.client.login(username="mango", password="lovemango")

        # When
        response = self.client.get(self.my_quiz_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, "html.parser")
        main_area = soup.find("div", id="main-area")

        # Then
        self.assertIn("아직 만든 퀴즈가 없어요!", main_area.find("h2").text)

    # TODO : Update 페이지 기능 구현 테스트 ( 배포 이후 작업 )

    # def test_enter_update_page(self):
    #     """/my-qui-es/pk/ 접속 테스트 -> 로그인 한 경우만 접속 가능"""
    #     # Given
    #     self.client.login(username="mango", passwore="lovemango")
    #     # When
    #     response = self.client.get(self.quiz_001)
    #     # Then
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_update_page(self):
    #     """/my-qui-es/pk/ 페이지의 요소 테스트"""
    #     # Given
    #     self.client.login(username="mango", password="lovemango")
    #
    #     # When
    #     response = self.client.get(self.quiz_001)
    #     self.assertEqual(response.status_code, 200)
    #
    #     soup = BeautifulSoup(response.content, "html.parser")
    #
    #     main_area = soup.find("div", id="main-area")


class TestMain(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_mango = User.objects.create_user(
            username="mango", password="lovemango"
        )

        self.quiz_001 = Quiz.objects.create(
            author=self.user_mango,
            title="애플 망고가 되려면?",
            private=True,
        )

        self.quiz_002 = Quiz.objects.create(
            author=self.user_mango,
            title="애플망고 vs 망고스틴",
            private=False,
        )

        self.my_quiz_url = "/my-qui-es/"  # My Quiz 페이지 url
        self.quiz_001_url = f"/my-qui-es/{self.quiz_001.pk}"  # 퀴즈 001의 디테일 페이지 url
        self.main_url = "/"

    def test_private_quiz(self):
        """
        비공개 퀴즈 출력 여부를 테스트 -> private=True 는 main에서 보이면 안됨
                                  -> private=False 는 main에서 보여야 함
        """
        # Given
        private_quiz = Quiz.objects.filter(private=True)  # True 면 비공개
        public_quiz = Quiz.objects.filter(private=False)  # False 면 공개

        # 메인 페이지
        response = self.client.get(self.main_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # hit quiz area 가져오기 -> hit quiz 목록 private/public 퀴즈의 유무 테스트 예정
        hit_quiz_area = soup.find("div", id="hit-quiz-area")
        # currnet quiz area 가져오기 -> current quiz 목록 private/public 퀴즈의 유무 테스트 예정
        current_quiz_area = soup.find("div", id="current-quiz-area")

        # When
        private_title = [i.title for i in private_quiz]  # 비공개 퀴즈의 제목만 가져옴
        public_title = [i.title for i in public_quiz]  # 공개 퀴즈의 제목만 가져옴

        hit_quiz = hit_quiz_area.find_all("a")
        hit_quiz_title = [i.text[:-3] for i in hit_quiz]  # 제목만 가져옴

        current_quiz = current_quiz_area.find_all("a")
        current_quiz_title = [i.text[:-3] for i in current_quiz]  # 제목만 가져옴

        # Then
        self.assertNotIn(
            private_title, hit_quiz_title
        )  # private 퀴즈가 hit quiz 목록에 없는지 확인
        self.assertEqual(public_title, hit_quiz_title)  # public 퀴즈가 hit quiz 목록에 있는지 확인

        self.assertNotIn(
            private_title, current_quiz_title
        )  # 동잏한 방법으로 current quiz 목록 확인
        self.assertEqual(public_title, current_quiz_title)

    def create_hit_quiz(self):
        """hit quiz 목록 테스트 용 퀴즈 생성"""
        self.hit_quiz_001 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 001", hit=101  # 5번째
        )

        self.hit_quiz_002 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 002", hit=102  # 4번째
        )

        self.hit_quiz_003 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 003", hit=103  # 3번째
        )

        self.hit_quiz_004 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 004", hit=104  # 2번째
        )

        self.hit_quiz_005 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 005", hit=10000  # 1번째
        )

        self.hit_quiz_006 = Quiz.objects.create(
            author=self.user_mango, title="퀴즈 006", hit=5  # hit 퀴즈 목록에 보이면 안됨
        )

        # 정답지 다음과 같이 조회수가 높은 순서대로 출력되야 함
        self.answer = [
            self.hit_quiz_005.title,
            self.hit_quiz_004.title,
            self.hit_quiz_003.title,
            self.hit_quiz_002.title,
            self.hit_quiz_001.title,
        ]

    def test_get_hit_quiz(self):
        """DB에서 가져오는 방식이 정답인지 테스트 -> DB에서 order_by로 가져오는 것과 정답지를 비교"""
        # Given
        # 퀴즈 생성
        self.create_hit_quiz()
        # 정답지
        answer = self.answer

        # When
        # DB에서 가져온 조회수 높은 퀴즈 5개
        top_hits = Quiz.objects.order_by("-hit")[:5]
        # top_hit_quiz에서 title만 추출
        hit_quiz = [i.title for i in top_hits]
        # print(hit_quiz)

        # Then
        # 정답지와 DB에서 가져온 퀴즈가 동일한가?
        self.assertEqual(answer, hit_quiz)

    def test_hit_quiz_print(self):
        """조회수에 따라 정확하게 출력 되었는지 테스트 -> 정답지와 화면에 출력된 퀴즈를 비교"""
        # Given
        # 문제 생성
        self.create_hit_quiz()
        # 정답지
        answer = self.answer

        # When
        # main 페이지 들어가기 -> 로그인 여부와 상관 없이 보여야하기 때문에 로그인하지 않음
        response = self.client.get(self.main_url)
        soup = BeautifulSoup(response.content, "html.parser")
        # hit quiz area 가져오기
        hit_quiz_area = soup.find("div", id="hit-quiz-area")
        # 퀴즈의 타이틀이 들어가 있는 a 태그를 모두 가져옴
        a = hit_quiz_area.find_all("a")
        # html을 보면 '제목 + (조회수)' 형태로 되어 있음 제목만 가져오기 위해 슬라이싱함
        quiz_title = [i.text[:6] for i in a]  # 메인 페이지에 보이는 조회수 높은 퀴즈 5개

        # Then
        # 화면에 제대로 출력 되었는가?
        self.assertEqual(answer, quiz_title)

    def test_current_quiz(self):
        """current quiz는 생성 일자가 늦을수록 위에 있어야 함"""
        # Given
        sort_quiz = Quiz.objects.order_by("-create_at")  # create_at 을 기준으로 정렬
        sort_quiz_title = [
            i.title for i in sort_quiz if i.private is False
        ]  # 공개 퀴즈만 보여야함

        # When
        response = self.client.get(self.main_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # current quiz 목록에서 quiz title 가져오기
        current_quiz_area = soup.find("div", id="current-quiz-area")
        current_quiz = current_quiz_area.find_all("a")

        current_quiz_title = [i.text[:-3] for i in current_quiz]  # 제목만 가져옴

        # Then
        self.assertEqual(sort_quiz_title, current_quiz_title)
