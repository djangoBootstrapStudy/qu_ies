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
        self.assertEqual(f"출제자: {self.quiz_001.author.username}", quiz_author.text)

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

    # 2. 시작하기 버튼 누르면 필적확인란이 같을경우 info(응시자와 오늘날짜)가 session에 들어가는지 확인
    def test_quiz_start_page_post_same_saying_info_in_session_check(self):
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


class SolveQuizTestView(TestCase):

    # TODO: SetUp
    # 퀴즈, 문제, 보기 생성
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

        # quiz_001_url
        self.quiz_001_url = f"/qui-es/{self.quiz_001.pk}/solving/"

        # 퀴즈시작페이지에서 session추가
        self.data = {
            "tester-name": "퀴즈가 좋아!",
            "test-date": date.today(),
            "follow-saying": "필적확인란",
            "saying": "필적확인란",
        }
        self.client.post(self.quiz_001.get_absolute_url(), self.data)

    # TODO: 문제풀기 페이지로 이동했을경우 quiz_solve 페이지 확인(GET)
    # 1. 퀴즈 문제 풀기 페이지 이동
    def test_enter_quiz_solve_page(self):
        # Given
        response = self.client.get(self.quiz_001_url)

        # When
        soup = BeautifulSoup(response.content, "html.parser")

        # Then
        self.assertEqual(self.quiz_001_url, "/qui-es/1/solving/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual("문제 풀기 페이지", soup.title.text)

    # 2. info(응시자, 응시일자 정보) 존재여부 확인
    def test_quiz_solve_page_get_info_in_session_check(self):
        # Given
        self.client.get(self.quiz_001_url)
        session = self.client.session

        # When
        """세션가져오기"""
        tester_name = session["tester_name"]
        test_date = session["test_date"]

        # Then
        self.assertEqual(tester_name, self.data["tester-name"])  # 응시자
        self.assertEqual(test_date, self.data["test-date"].strftime("%Y-%m-%d"))  # 응시일자

    # 3. quiz의 테스트 제목, 출제자 확인
    def test_quiz_solve_page_get_quiz_check(self):
        # Given
        response = self.client.get(self.quiz_001_url)

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
        self.assertEqual(f"출제자: {self.quiz_001.author.username}", quiz_author.text)

    # 4. quiz의 문제수 10개인지 확인, 문제 일치 확인
    def test_quiz_solve_page_get_question_check(self):
        # Given
        response = self.client.get(self.quiz_001_url)
        quiz_question = QuizQuestion.objects.filter(quiz=self.quiz_001)

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        all_question_div = soup.find_all("div", id="question")

        # Then
        """
        퀴즈의 문제개수 10개인지 확인
        퀴즈의 문제내용 일치하는지 10개 모두 확인(for문돌리기)
        """
        self.assertEqual(len(all_question_div), 10)
        for question_num in range(1, 11):
            question_div = soup.find("div", id=f"question{question_num}")
            self.assertEqual(question_div.text, f"문제{question_num}번 내용")

    # 5. quiz의 보기수 40개인지 확인, 문제 1,10번만 보기확인
    def test_quiz_solve_page_get_example_check(self):
        # Given
        response = self.client.get(self.quiz_001_url)

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        all_example_div = soup.find_all("div", id="example")

        # Then
        """
        보기개수가 총 40개인지 확인(문제10*보기4)
        문제 1번의 보기내용이 일치한지 확인(for문)
        문제 10번의 보기내용이 일치한지 확인(for문)
        """
        self.assertEqual(len(all_example_div), 40)
        for example_num in range(1, 4):
            no1_example_div = soup.find("div", id=f"q1_{example_num}")
            self.assertEqual(no1_example_div.text, f"문제1-보기{example_num}번 내용")

        for example_num in range(1, 4):
            no10_example_div = soup.find("div", id=f"q10_{example_num}")
            self.assertEqual(no10_example_div.text, f"문제10-보기{example_num}번 내용")

    # 6. quiz의 각 question의 보기수가 4개인지 모두 확인
    def test_quiz_solve_page_get_each_question_examples_is_four(self):
        # Given
        response = self.client.get(self.quiz_001_url)

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        all_question_div = soup.find_all("div", id="quiz")

        question_num = 0
        for question in all_question_div:

            question_num += 1
            """문제 1개"""
            question_div = question.find("div", id="question")
            question_span = question_div.find("span")
            """문제의 보기 4개"""
            example_div = question.find_all("div", id="example")

            # Then
            """
            몇번 문제인지 확인
            각 문제의 보기가 4개인지 확인(for문)
            """
            self.assertEqual(question_span.text, f"Q{question_num}.")
            self.assertEqual(len(example_div), 4)

    # 7. 선택한 답의 수는 아직 없으므로 0인지 확인
    def test_quiz_solve_page_get_zero_example_check(self):
        # Given
        response = self.client.get(self.quiz_001_url)

        # When
        soup = BeautifulSoup(response.content, "html.parser")
        select_answer = soup.find("div", id="select-answer")

        # Then
        self.assertEqual(select_answer.text, "0")

    # TODO: 문제풀기 페이지로 이동했을경우 quiz_solve 페이지 확인(POST)
    # 1. 그만두기 버튼 누르면 메인페이지로 이동 확인
    # def test_quiz_solve_page_post_main_button(self):
    #     # Given
    #     response = self.client.get(self.quiz_001_url)
    #
    #     # When
    #     soup = BeautifulSoup(response.content, "html.parser")
    #     '''버튼누르기'''
    #     main_button = soup.find("input", type="button")
    #
    #     # Then
    #     if main_button.attrs["value"] == "그만두기":
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual("Qui_es?", soup.title.text)

    # 2. 완료 버튼 누르면 정답 세션에 저장 후 세션 확인, 저장된 세션의 답이 10개인지 확인
    def test_quiz_solve_page_post_answer_session_check(self):
        # Given
        """각 문제의 답 세션에 저장"""
        data = {
            "question1_answer": 1,
            "question2_answer": 2,
            "question3_answer": 3,
            "question4_answer": 4,
            "question5_answer": 1,
            "question6_answer": 2,
            "question7_answer": 3,
            "question8_answer": 4,
            "question9_answer": 1,
            "question10_answer": 2,
        }
        # When
        self.client.post(self.quiz_001_url, data)
        session = self.client.session
        answer = session["answer"]

        # Then
        """
        세션에 저장된 답 10개인지 확인
        세션에 저장된 답 일치하는지 확인
        """
        self.assertEqual(len(answer), 10)
        for question_no in range(1, 11):
            self.assertEqual(
                data[f"question{question_no}_answer"], answer[str(question_no)]
            )

    # 3. 완료 버튼 누르면 답확인 페이지로 이동 확인
    def test_quiz_solve_page_post_enter_quiz_result_page(self):
        # Given
        data = {
            "question1_answer": 1,
            "question2_answer": 2,
            "question3_answer": 3,
            "question4_answer": 4,
            "question5_answer": 1,
            "question6_answer": 2,
            "question7_answer": 3,
            "question8_answer": 4,
            "question9_answer": 1,
            "question10_answer": 2,
        }

        # When
        response = self.client.post(self.quiz_001_url, data)

        # Then
        self.assertEqual(response.url, "/qui-es/1/result/")

    # TODO: 답확인 페이지로 이동했을 경우 quiz_solve_done 페이지 확인
    # 1. 응시자의 성명, 응시일자 정보 확인
