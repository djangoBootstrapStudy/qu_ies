function getCheckedCnt()  {
  // 선택된 목록 가져오기
  const query = 'input[id="exampleRadios"]:checked';
  const selectedElements =
      document.querySelectorAll(query);

  // 선택된 목록의 갯수 세기
  const selectedElementsCnt =
        selectedElements.length;

  // 출력
  document.getElementById('select-answer').innerText
    = selectedElementsCnt;
}