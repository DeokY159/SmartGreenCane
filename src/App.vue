<template>
  <div>
    <header>
      <nav-bar id="nav" />
    </header>
    <div id="about_section">
      <h2>About Green Cane</h2>
    </div>
    <div id="app">
      <div id="profile_section">
        <div id="profile">
          <img src="@/assets/profile.png" alt="Profile Picture" id="profile_picture" />
          <div id="profile_info">
            <p><b>홍길동</b> / 여</p>
            <p>1997.05.16</p>
          </div>
        </div>
      </div>
      <div id="map_section">
        <div id="map"></div>
      </div>
      <div id="right_section">
        <div id="gps_info">
          <h3>GPS</h3>
          <img :src="require('@/assets/gps.png')" alt="GPS Icon" class="icon" />
        </div>
        <div id="battery_info">
          <h3>Battery</h3>
          <img :src="require('@/assets/battery.png')" alt="Battery Icon" class="icon" />
        </div>
        <div id="impact_info">
          <h3>Impact</h3>
          <img :src="require('@/assets/impact.png')" alt="Impact Icon" class="icon" @click="showPopup" />
        </div>
        <div id="sound_info">
          <h3>Sound</h3>
          <img :src="require('@/assets/sound.png')" alt="Sound Icon" class="icon" />
        </div>
      </div>
    </div>
    <!-- Popup Component -->
    <Popup v-if="isPopupVisible" :impactValue="22" @close="isPopupVisible = false" />
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import navBar from './components/navBar.vue';
import Popup from './components/Popup.vue';

export default {
  name: 'App',
  components: {
    navBar,
    Popup,
  },
  data() {
    return {
      userLocation: [37.5507583, 127.0741682], // 초기 사용자 좌표
      map: null,
      isPopupVisible: false, // Popup visibility 상태
    };
  },
  methods: {
    updateLocation(lat, lng) {
      this.userLocation = [lat, lng];
      this.map.setView(this.userLocation, 16); // 지도 중심 이동
    },
    showPopup() {
      this.isPopupVisible = true; // Popup을 표시
    },
  },
  mounted() {
    // 지도 생성
    this.map = L.map('map').setView(this.userLocation, 16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.map);

    // 커스텀 아이콘 생성
    const customIcon = L.icon({
      iconUrl: require('@/assets/custom-marker.png'), // 이미지 경로 (assets 폴더에 저장된 파일)
      iconSize: [32, 32], // 아이콘 크기
      iconAnchor: [16, 32], // 아이콘 앵커 위치
      popupAnchor: [0, -32], // 팝업 위치
    });

    // 초기 마커 생성
    const marker = L.marker(this.userLocation, { icon: customIcon })
      .addTo(this.map)
      .bindPopup('<b>사용자 위치</b><br>현재 위치입니다.')
      .openPopup();

    // GeoJSON 데이터 추가
    const geojsonData = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [126.978, 37.5665], // 서울 좌표
          },
          properties: {
            name: 'Seoul City',
          },
        },
      ],
    };

    L.geoJSON(geojsonData, {
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: 8,
          fillColor: 'blue',
          color: 'blue',
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8,
        });
      },
    }).addTo(this.map);
  },
};
</script>


<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  height: 100vh; /* 화면 전체 높이를 설정 */
  overflow: hidden; /* 스크롤바를 없앰 */
}

/* 전체 레이아웃 */
#app {
  margin: 0; /* 외부 여백 제거 */
  padding: 0; /* 내부 패딩 제거 */
  display: flex;
  flex-direction: row;
  height: calc(100vh - 50px); /* 헤더 높이를 제외한 화면 높이 */
}

#map_section {
  display: flex;
  justify-content: center; /* 가로 가운데 정렬 */
  align-items: center; /* 세로 가운데 정렬 */
  flex: 1; /* 남은 공간을 차지 */
  height: calc(100vh - 120px); /* About Green Cane 섹션 아래 높이 */
  margin-top: 45px; /* 헤더와 About 섹션 높이를 제외한 위치 */
  margin-right: 0%; /* 오른쪽 여백을 고정 */
  margin-left: 0%;
  padding: 0; /* 내부 여백 제거 */
}

#map {
  width: 80%; /* 부모 섹션의 너비를 차지 */
  height: 100%; /* 부모 섹션의 높이를 차지 */
  border-radius: 10px; /* 둥근 테두리 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
}

#main_title h1 {
  margin-bottom: 0;
}

#main_title {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 1%;
}

/* 왼쪽 프로필 섹션 */
#profile_section {
  width: 13%; /* 프로필 섹션 너비 */
  background-color: #eaf5e9;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px; /* 내부 여백 */
  border-right: 2px solid #c3e6cb;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
  height: 100vh; /* 전체 화면 높이를 차지 */
  margin: 0; /* 외부 여백 제거 */
}

#profile_info {
  text-align: center; /* 텍스트 중앙 정렬 */
  margin: 0; /* 외부 여백 제거 */
  padding: 0; /* 내부 여백 제거 */
}

#profile_info p:first-child {
  font-size: 20px; /* 홍길동 / 여의 글씨 크기 */
  font-weight: bold; /* 강조 */
  margin: 0 0 5px 0; /* 아래쪽에 약간의 간격 추가 */
  padding: 0; /* 내부 패딩 제거 */
}

#profile_info p:last-child {
  font-size: 16px; /* 생년월일의 글씨 크기 */
  color: #555; /* 약간 흐린 색상 */
  margin: 5px 0 0 0; /* 위쪽에 약간의 간격 추가 */
  padding: 0; /* 내부 패딩 제거 */
}
#profile_picture {
  width: 90px; /* 프로필 사진 크기 */
  height: 90px;
  border-radius: 50%; /* 원형 사진 */
  margin-bottom: 15px; /* 사진과 텍스트 사이 간격 */
  margin: 0 auto 15px auto; /* 위, 양옆 중앙 정렬 */
  display: block; /* block으로 설정하여 가로 중앙 정렬 적용 */
}

/* About Green Cane 섹션 */
#about_section {
  text-align: left;
  background-color: #d9f2e6; /* 연한 초록색 배경 */
  padding: 10px 0; /* 상하 여백 */
  border-bottom: 2px solid #c3e6cb; /* 아래쪽 테두리 */
  font-family: Arial, sans-serif;
  width: calc(100% - 12%); /* 프로필 섹션을 제외한 나머지 공간 차지 */
  margin-left: 13.9%; /* 프로필 섹션 만큼 왼쪽 여백 추가 */
  position: absolute; /* 겹침 방지 */
  top: 69px; /* 헤더 바로 아래에 위치 */
  z-index: 1; /* 다른 요소 위에 표시 */
}

#about_section h2 {
  margin: 0;
  font-size: 20px;
  color: #4d4d4d; /* 텍스트 색상 */
  font-weight: normal; /* 가벼운 글씨체 */
  padding-left: 20px;
}

#right_section {
  width: 13%; /* 오른쪽 섹션의 너비 */
  background-color: #eaf5e9; /* 배경색 */
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  align-items: center; /* 가로 가운데 정렬 */
  padding: 15px; /* 내부 여백 */
  border-left: 2px solid #c3e6cb; /* 왼쪽 테두리 */
  box-shadow: -2px 0px 5px rgba(0, 0, 0, 0.1); /* 왼쪽 그림자 */
  height: calc(100vh - 120px); /* 상단 섹션을 제외한 화면 높이 */
  position: absolute; /* 위치를 고정 */
  right: 0; /* 오른쪽 끝에 붙임 */

  top: 110px; /* Green cane management application + About Green Cane의 높이 */
}

/* 공통 아이콘 스타일 */
.icon {
  width: 70px;
  height: 70px;
  margin: 10px 0;
  display: block;
}

/* 섹션별 스타일링 */
#gps_info, #battery_info, #impact_info, #sound_info {
  margin-bottom: 20px;
  text-align: center;
}

#gps_info h3, #battery_info h3, #impact_info h3, #sound_info h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

</style>