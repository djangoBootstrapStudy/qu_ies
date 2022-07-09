from datetime import date

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import Client, TestCase

from make_quiz.models import QuizExample, QuizQuestion
from my_quiz.models import Quiz


# Create your tests here.
class StartQuizTestView(TestCase):

    # TODO: SetUp
    # 퀴즈 하나 만들기
    def setUp(self):
        self.client = Client()

        # 유저
        self.user = User.objects.create(username="LoveQuiz", password="lovequiz1234")

        # 퀴즈 1개
        self.quiz_001 = Quiz.objects.create(author=self.user, title="나를 맞춰봐!")

        # 문제 10개
        for question_num in range(1, 11):
            self.quiz_001_question = QuizQuestion.objects.create(
                quiz=self.quiz_001, no=question_num, content=f"문제{question_num}번 내용"
            )

            # 한 문제당 보기 4개
            for example_num in range(1, 5):
                QuizExample.objects.create(
                    question=self.quiz_001_question,
                    no=example_num,
                    content=f"문제{question_num}-보기{example_num}번 내용",
                )

            # 답(무조건 1번)
            self.quizexample_answer = QuizExample.objects.get(
                question=self.quiz_001_question, no=1
            )
            self.quizexample_answer.answer = True
            self.quizexample_answer.save()

    # TODO: 문제 시작하기 페이지 이동했을경우 quiz_start 페이지 확인(GET)
    # 1. 로그인 확인 여부없이 quiz_start 페이지로 이동 확인
    def test_enter_quiz_start_page(self):
        # Given
        response = self.client.get(self.quiz_001.get_absolute_url())

        # When
        soup = BeautifulSoup(response.content, "html.parser")

        # Then
        self.assertEqual(self.quiz_001.get_absolute_url(), "/qui-es/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("문제 시작 페이지", soup.title.text)

    # 2. quiz의 테스트 제목, 출제자 확인
    def test_quiz_start_page_get_title_and_user_check(self):
        # Given
        response = self.client.get(self.quiz_001.get_absolute_url())

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        quiz_title = soup.find("div", id="quiz-title")
        quiz_author = soup.find("div", id="quiz-author")

        # Then
        """
        response시 pk에 맞는 quiz object 인지 확인
        quiz의 문제 제목 확인
        quiz의 문제 출제자 확인
        """
        self.assertEqual(response.context["quiz"], self.quiz_001)
        self.assertEqual(self.quiz_001.title, quiz_title.text)
        self.assertEqual(self.quiz_001.author.username, quiz_author.text)

    # 3. 필적확인란 랜덤 명언 값 존재하는지 확인하기
    def test_quiz_start_page_get_random_saying_check(self):
        # Given
        response = self.client.get(self.quiz_001.get_absolute_url())

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        saying = soup.find("div", id="random-saying")

        # Then
        """response로 보낸 명언과 html의 명언 일치확인"""
        self.assertEqual(response.context["saying"], saying.text)

    # TODO: 문제 시작하기 페이지 이동했을경우 quiz_start 페이지 확인(POST)
    # 1. 시작하기 버튼 누르면 필적확인란 값이 다를경우 재로드 확인
    def test_quiz_start_page_post_diffrent_saying_check(self):
        # Given
        response = self.client.get(self.quiz_001.get_absolute_url())
        saying = response.context["saying"]
        data = {
            "saying": saying,
            "follow-saying": "제시된 필적확인란과 다르게 적음",
        }

        # When
        self.client.post(self.quiz_001.get_absolute_url(), data)
        soup = BeautifulSoup(response.content, "html.parser")

        # Then
        """
        필적확인란 값이 다른지 확인
        quiz_start.html 재로드
        """
        self.assertNotEqual(data["saying"], data["follow-saying"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual("문제 시작 페이지", soup.title.text)

    # 2. 시작하기 버튼 누르면 필적확인란이 같을경우 응시자와 오늘날짜가 session에 들어가는지 확인
    def test_quiz_start_page_post_same_saying_tester_and_today_in_session_check(self):
        # Given
        response = self.client.get(self.quiz_001.get_absolute_url())
        saying = response.context["saying"]

        data = {
            "tester-name": self.user.username,
            "test-date": date.today(),
            "follow-saying": saying,
            "saying": saying,
        }

        # When
        self.client.post(self.quiz_001.get_absolute_url(), data)
        session = self.client.session
        tester_name = session["tester_name"]
        test_date = session["test_date"]

        # Then
        """
        세션에 저장된 응시자 성명 확인
        세션에 저장된 응시일자가 오늘인지 확인
        """
        self.assertEqual(tester_name, data["tester-name"])
        self.assertEqual(test_date, data["test-date"].strftime("%Y-%m-%d"))

    # 3. 시작하기 버튼 누르면 필적확인란이 같을경우 quiz_solve 페이지로 이동 확인
    def test_quiz_start_page_post_same_saying_enter_quiz_page(self):
        # Given
        get_response = self.client.get(self.quiz_001.get_absolute_url())
        saying = get_response.context["saying"]

        data = {
            "tester-name": self.user.username,
            "test-date": date.today(),
            "follow-saying": saying,
            "saying": saying,
        }

        # When
        post_response = self.client.post(self.quiz_001.get_absolute_url(), data)

        # Then
        self.assertEqual(post_response.url, "/qui-es/1/solving/")

    # TODO: 문제풀기 페이지로 이동했을경우 quiz_solve 페이지 확인
    # 1. quiz의 테스트 제목, 출제자 확인
    # 2. 응시자의 성명, 응시일자 정보 존재여부 확인
    # 3. quiz의 문제수 10개인지 확인, 문제 일치 확인
    # 4. quiz의 보기수 40개인지 확인, 각 문제 보기 1번 확인
    # 5. 선택한 답의 수가 완료문항수와 같은지 확인

    # TODO: 버튼 확인
    # 1. 그만두기 버튼 누르면 메인페이지로 이동 확인
    # 2. 완료버튼
    #   완료 버튼 누르면 quiz의 선택한 정답수 10개인지 확인
    #   완료 버튼 누르면 답확인 페이지로 이동 확인

    # TODO: 답확인 페이지로 이동했을 경우 quiz_solve_done 페이지 확인
    # 1. 응시자의 성명, 응시일자 정보 확인
