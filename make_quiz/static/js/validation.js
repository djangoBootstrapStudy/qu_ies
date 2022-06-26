function Checkform() {
    if( frm.title.value == "" ) {

        frm.title.focus();
        alert("퀴즈제목을 입력해 주십시오.");

        return false;

    }

    // 문제 & 보기 확인
    //1
    if( frm.question1.value == "" ) {
        frm.question1.focus();

        alert("1번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q1_1.value == "" || frm.q1_2.value == ""||frm.q1_3.value == ""||frm.q1_4.value == "") {

        frm.question1.focus();
        alert("문제1번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //2
    if( frm.question2.value == "" ) {
        frm.question2.focus();

        alert("2번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q2_1.value == "" || frm.q2_2.value == ""||frm.q2_3.value == ""||frm.q2_4.value == "") {
        frm.question2.focus();
        alert("문제2번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //3
    if( frm.question3.value == "" ) {
        frm.question3.focus();

        alert("3번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q3_1.value == "" || frm.q3_2.value == ""||frm.q3_3.value == ""||frm.q3_4.value == "") {
        frm.question3.focus();
        alert("문제3번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //4
    if( frm.question4.value == "" ) {
        frm.question4.focus();

        alert("4번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q4_1.value == "" || frm.q4_2.value == ""||frm.q4_3.value == ""||frm.q4_4.value == "") {
        frm.question4.focus();
        alert("문제4번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //5
    if( frm.question5.value == "" ) {
        frm.question5.focus();

        alert("5번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q5_1.value == "" || frm.q5_2.value == ""||frm.q5_3.value == ""||frm.q5_4.value == "") {
        frm.question5.focus();
        alert("문제5번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //6
    if( frm.question6.value == "" ) {
        frm.question6.focus();

        alert("6번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q6_1.value == "" || frm.q6_2.value == ""||frm.q6_3.value == ""||frm.q6_4.value == "") {
        frm.question6.focus();
        alert("문제6번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //7
    if( frm.question7.value == "" ) {
        frm.question7.focus();

        alert("7번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q7_1.value == "" || frm.q7_2.value == ""||frm.q7_3.value == ""||frm.q7_4.value == "") {
        frm.question7.focus();
        alert("문제7번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //8
    if( frm.question8.value == "" ) {
        frm.question8.focus();

        alert("8번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q8_1.value == "" || frm.q8_2.value == ""||frm.q8_3.value == ""||frm.q8_4.value == "") {
        frm.question8.focus();
        alert("문제8번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //9
    if( frm.question9.value == "" ) {
        frm.question9.focus();

        alert("9번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q9_1.value == "" || frm.q9_2.value == ""||frm.q9_3.value == ""||frm.q9_4.value == "") {
        frm.question9.focus();
        alert("문제9번 보기를 모두 입력해야 합니다.");

        return false;

    }

    //10
    if( frm.question10.value == "" ){
        frm.question10.focus();

        alert("10번 문제를 입력해 주십시오.");

        return false;
    }
    if( frm.q10_1.value == "" || frm.q10_2.value == ""||frm.q10_3.value == ""||frm.q10_4.value == "") {
        frm.question10.focus();
        alert("문제10번 보기를 모두 입력해야 합니다.");

        return false;

    }

}
