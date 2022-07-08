from django.test import TestCase,Client
from django.contrib.auth.models import User
from my_quiz.models import Quiz
from make_quiz.models import QuizQuestion,QuizExample

# Create your tests here.
class SolveQuizTestView(TestCase):

    # TODO: SetUp
    # 퀴즈 하나 만들기
    def setUp(self):
        self.client=Client()

        #유저
        self.user=User.objects.create(username='LoveQuiz',password='lovequiz1234')

        #퀴즈 1개
        self.my_quiz=Quiz.objects.create(author=self.user,title='나를 맞춰봐!')

        #문제 10개
        for question_num in range(1,11):
            self.my_quiz_question=QuizQuestion.objects.create(quiz=self.my_quiz,no=question_num,content=f'문제{question_num}번 내용')

            #한 문제당 보기 4개
            for example_num in range(1,5):
                QuizExample.objects.create(question=self.my_quiz_question,no=example_num,content=f'문제{question_num}-보기{example_num}')

            #답
            self.quiz_answer = QuizExample.objects.get(question=self.my_quiz_question, no=1)
            self.quiz_answer.answer = True
            self.quiz_answer.save()



    # TODO: 문제 시작하기 페이지 이동했을경우 quiz_start 페이지 확인
    # 1. 로그인 확인 여부없이 quiz_start 페이지로 이동 확인
    # 2. quiz의 테스트 제목, 출제자 확인
    # 3. 필적확인란 랜덤 명언 값 존재하는지 확인하기
    # 4. 시작하기 버튼
    #   시작하기 버튼 누르면 성명, 응시일자 저장되는지 확인
    #   시작하기 버튼 누르면 필적확인란 값 일치하는지 확인
    #   시작하기 버튼 누르면 quiz_solve 페이지로 이동 확인

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
