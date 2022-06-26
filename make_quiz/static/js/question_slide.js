let quizIndex=0;
let position=0;
const quiz_width=400;
const btnPrevious=document.querySelector(".previous")
const btnNext=document.querySelector(".next")
const quiz=document.querySelector(".slide-quiz")

function prev(){
    if (quizIndex>0){
        btnNext.removeAttribute("disabled")
        position+=quiz_width;
        quiz.style.transform = `translateX(${position}px)`;
        quizIndex=quizIndex-1;

    }
    if (quizIndex == 0){
        btnPrevious.setAttribute('disabled','true')

    }
}
function next(){
    if (quizIndex < 9) {
        btnPrevious.removeAttribute("disabled")
        position -= quiz_width;
        quiz.style.transform = `translateX(${position}px)`;
        quizIndex = quizIndex + 1;

    }
    if (quizIndex == 9) {
        btnNext.setAttribute('disabled', 'true')

    }
}
function init(){
    btnPrevious.setAttribute('disabled','true')
    btnPrevious.addEventListener("click",prev)
    btnNext.addEventListener("click",next)

}

init();