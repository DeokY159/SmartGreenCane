<template>
    <div class="popup-overlay">
      <div class="popup-container">
        <div class="popup-content">
          <img :src="require('@/assets/위험지역아이콘.png')" alt="Impact Icon" class="impact-icon" />
          <h2 class="popup-title">Danger Zone Alert!</h2>
          <p class="popup-description">
            Multiple impact warnings detected within 20 meters.<br />
            This area has been identified as a hazardous zone.<br />
            Please proceed with caution.
          </p>
        </div>
        <div class="popup-buttons">
          <!--<button class="sound-btn" @click="$emit('close')">🔊 Send Sound Alert</button>-->
          <button class="sound-btn">🔊 Send Sound Alert</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Popup", // 컴포넌트 이름
  };
  </script>
  
  <style scoped>
  /* 팝업 배경 스타일 */
  .popup-overlay {
    position: fixed; /* 화면에 고정 */
    top: 0;
    left: 0;
    width: 100%; /* 전체 화면 너비 */
    height: 100%; /* 전체 화면 높이 */
    background-color: rgba(255, 0, 0, 0);
    display: flex; /* 중앙 정렬을 위해 flex 사용 */
    justify-content: center; /* 가로 중앙 정렬 */
    align-items: center; /* 세로 중앙 정렬 */
    z-index: 1000; /* 다른 요소 위에 표시 */
  }
  
  /* 팝업 컨테이너 스타일 */
  .popup-container {
    background: #fff; /* 흰색 배경 */
    border-radius: 10px; /* 둥근 테두리 */
    width: 400px; /* 고정된 너비 */
    padding: 20px; /* 내부 여백 */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); /* 그림자 효과 */
    text-align: center; /* 텍스트 중앙 정렬 */
  }
  
  /* 팝업 내용 섹션 스타일 */
  .popup-content {
    margin-bottom: 20px; /* 버튼과의 간격 */
  }
  
  /* 아이콘 스타일 */
  .impact-icon {
    width: 90px; /* 너비 */
    height: 90px; /* 높이 */
    margin: 0 auto 15px auto; /* 상하좌우 중앙 정렬 */
    display: block; /* block 요소로 변경해 가로 정렬 */
  }
  
  /* 제목 스타일 */
  .popup-title {
    font-size: 22px; /* 글자 크기 */
    font-weight: bold; /* 글자 두께 */
    margin-bottom: 10px; /* 아래 여백 */
    color: #ff0000; /* 빨간색 */
    font-weight: bold; /* 굵은 텍스트 */
  }
  
  /* 설명 텍스트 스타일 */
  .popup-description {
    font-size: 16px; /* 글자 크기 */
    color: #666; /* 회색 텍스트 */
  }
  
  /* 버튼 섹션 스타일 */
  .popup-buttons {
    display: flex; /* flex 사용 */
    justify-content: center; /* 버튼을 가운데 정렬 */
  }
  
  /* OK 버튼 스타일 */
  .sound-btn {
    background-color: #da3f3f; /* 초록색 배경 */
    color: #fff; /* 흰색 글자 */
    font-size: 16px; /* 글자 크기 */
    border: none; /* 테두리 제거 */
    border-radius: 5px; /* 둥근 버튼 */
    padding: 10px 20px; /* 내부 여백 */
    cursor: pointer; /* 마우스 포인터 변경 */
  }
  
  /* OK 버튼 호버 효과 */
  .sound-btn:hover {
    background-color: #8d1313; /* 더 진한 파란색 배경 */
  }
  </style>
  