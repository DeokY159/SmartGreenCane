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
            <p><b>Hong Gil Dong</b> / Female</p>
            <p>1997.05.16</p>
          </div>
        </div>
        <hr class="divider" />
        <div id="info_section">
          <p>We provide a service that determines whether the user of Green Cane is in danger and sends a notification to the carer. We aims to make life safer for the blind people.</p>
        </div>
        <hr class="divider" />
        <div id="weather_section">
          <h3>Weather info</h3>
          <div id="weather_icon">
            <img src="@/assets/sun.png" alt="Sun Icon" class="icon" />
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
          <div class="info_box"><p>{{ gpsData_N }}</p></div>
          <div class="info_box"><p>{{ gpsData_E }}</p></div>
        </div>
        <div id="battery_info">
          <h3>Battery</h3>
          <img :src="require('@/assets/Battery.png')" alt="Battery Icon" class="icon" @click="showBatteryPopup"/>
          <div class="info_box"><p>{{ batteryData }}%</p></div>
        </div>
        <div id="impact_info">
          <h3>Impact</h3>
          <img :src="require('@/assets/impact.png')" alt="Impact Icon" class="icon" @click="showPopup" />
          <div class="info_box"><p>{{ impcatData }}</p></div>
        </div>
        <div id="sound_info">
          <h3>Sound</h3>
          <img :src="require('@/assets/sound.png')" alt="Sound Icon" class="icon" />
        </div>
      </div>
    </div>
    <!-- Battery Popup -->
    <BatteryPopup v-if="isBatteryPopupVisible" @close="isBatteryPopupVisible = false" />
    <!-- Impact Popup -->
    <Popup v-if="isPopupVisible" :impactValue="22" @close="isPopupVisible = false" />
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import navBar from './components/navBar.vue'
import Popup from './components/Popup.vue'
import BatteryPopup from "./components/BatteryPopup.vue";
import {fetchData,fetch_aeData} from './components/Importing.js'

export default {
  name: 'App',
  components: {
    navBar,
    Popup,
    BatteryPopup
  },
  data () {
    return {
      userLocation: [37.5507583, 127.0741682], // 초기 사용자 좌표
      map: null,
      marker : null,
      isPopupVisible: false, // Popup visibility 상태
      isBatteryPopupVisible: false, // Battery Popup 상태
      gpsData_N : null,
      gpsData_E : null,
      batteryData : null,
      impcatData : null, 
      soundData : "off",
      betterypopupShown: false,
      impacntopoupShown: false,
    }
  },
  methods: {
    updateLocation (lat, lng) {
      this.userLocation = [lat, lng]
      this.map.flyTo(this.userLocation, 16) // 지도 중심 이동  
      this.marker.setLatLng(this.userLocation);
    },

    showPopup () {
      this.isPopupVisible = true // Popup을 표시
    },
    showBatteryPopup() {
      this.isBatteryPopupVisible = true; // Battery Popup 표시
    },

    // tinyIoT에서 gps 센서 데이터 업데이트
    async updategpsSensorData () {
      const resources = 'gps'
      const gpsconValue = await fetchData(resources);
      console.log('받아온 GPS 데이터:', gpsconValue); // 받은 데이터 확인
      const parsedLocation = JSON.parse(gpsconValue);
      this.gpsData_N = parsedLocation[0];
      this.gpsData_E = parsedLocation[1];
      this.updateLocation(parsedLocation[0], parsedLocation[1]);
      console.log("각각 데이터", this.gpsData_N, this.gpsData_E);
      console.log('GPS 데이터로 userLocation 업데이트 완료:', this.userLocation);
    },

    // tinyIoT에서 becane 하위의 speed 센서 데이터 업데이트
    async updatespeedSensorData () {
      const resources = 'speed'
      const speedconValue = await fetchData(resources);
      console.log('받아온 speed 데이터:', speedconValue); // 받은 데이터 확인
    },

    // tinyIoT에서 becane 하위의 shock 센서 데이터 업데이트
    async updateshockSensorData () {
      const resources = 'shock'
      const shockconValue = await fetchData(resources);
      console.log('받아온 shock 데이터:', shockconValue); // 받은 데이터 확인

      if(shockconValue === 'is' && !this.impacntopoupShown){
        this.isPopupVisible = true;
        this.impacntopoupShown = true;
      }
    },

    // tinyIoT에서 becane 하위의 onoff 센서 데이터 업데이트
    async updateonoffSensorData () {
      const resources = 'onoff'
      const onoffconValue = await fetchData(resources);
      console.log('받아온 onoff 데이터:', onoffconValue); // 데이터 확인
      console.log('현재 Popup 상태:', this.betterypopupShown); // 플래그 상태 확인
      this.onoffData = onoffconValue;

      if (this.onoffData === 'off' && !this.betterypopupShown){
        this.isBatteryPopupVisible = true;
        this.betterypopupShown = true;
        console.log('배터리 팝업이 표시되었습니다'); // 로그 확인
      }
    },

    // tinyIoT에서 cane1 하위의 배터리센서의 데이터를 업데이트
    async updateBatteryData () {
      const resources = 'battery'
      const BatteryValue = await fetch_aeData(resources);
      this.batteryData = BatteryValue;
      console.log("받아온 배터리 데이터", BatteryValue);
    },

    // tinyIoT에서 cane1 하위의 impact 센서의 데이터를 업데이트
    async updateImpactData () {
      const resources = 'impact'
      const ImpactValue = await fetch_aeData(resources);
      this.impcatData = ImpactValue;
      console.log("받아온 임팩트 데이터", ImpactValue);
    },

    // tinyIoT에서 cane1 하위의 sound 센서의 데이터를 업데이트
    async updateSoundData () {
      const resources = 'sound'
      const SoundValue = await fetch_aeData(resources);
    }

  },

  mounted () {
    // 지도 생성
    this.map = L.map('map').setView(this.userLocation, 16)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map)

    
    // 커스텀 아이콘 생성
    const customIcon = L.icon({
      iconUrl: require('@/assets/custom-marker.png'), // 이미지 경로 (assets 폴더에 저장된 파일)
      iconSize: [32, 32], // 아이콘 크기
      iconAnchor: [16, 32], // 아이콘 앵커 위치
      popupAnchor: [0, -32] // 팝업 위치
    })

    // 초기 마커 생성
    this.marker = L.marker(this.userLocation, { icon: customIcon })
      .addTo(this.map)
      .bindPopup('<b>User Location</b><br>This is user\'s current location.')
      .openPopup()


    this.updategpsSensorData();
    this.updatespeedSensorData();
    this.updateshockSensorData();
    this.updateonoffSensorData();
    this.updateBatteryData();
    this.updateImpactData ();
    this.updateSoundData();

    setInterval(() => {
      this.updategpsSensorData();
      this.updatespeedSensorData();
      this.updateshockSensorData();
      this.updateonoffSensorData();
      this.updateBatteryData();
      this.updateImpactData();
      this.updateSoundData();
    }, 5000);
  }

}
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
  flex: 1; /* 남은 공간을 차지 */
  height: calc(100vh - 120px); /* About Green Cane 섹션 아래 높이 */
  margin-top: 45px;
  padding: 0; /* 내부 여백 제거 */
}

#map {
  width: 90%; /* 부모 섹션의 너비를 차지 */
  height: 99%; /* 부모 섹션의 높이를 차지 */
  margin-top: 5px;    /* 위쪽 여백 */
  margin-bottom: 5px; /* 아래쪽 여백 */
  margin-left: 7px;   /* 왼쪽 여백 */
  margin-right: 5px;  /* 오른쪽 여백 */
  border-radius: 5px; /* 둥근 테두리 */

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
  background-color: #dde9dc;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px; /* 내부 여백 */
  border-right: 2px solid #b8d8bf;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
  height: 100vh; /* 전체 화면 높이를 차지 */
  margin: 0; /* 외부 여백 제거 */
}

#profile_info {
  transform: translateY(35px); /* 아이콘을 35px 아래로 이동 */
  text-align: center; /* 텍스트 중앙 정렬 */
  margin: 0; /* 외부 여백 제거 */
  padding: 0; /* 내부 여백 제거 */

}

#profile_info p:first-child {
  font-size: 15px; /* 홍길동 / 여의 글씨 크기 */
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
  background-color: #ffffff;
  transform: translateY(35px); /* 아이콘을 35px 아래로 이동 */
  width: 90px; /* 프로필 사진 크기 */
  height: 90px;
  border-radius: 50%; /* 원형 사진 */
  margin-bottom: 15px; /* 사진과 텍스트 사이 간격 */
  margin: 0 auto 15px auto; /* 위, 양옆 중앙 정렬 */
  display: block; /* block으로 설정하여 가로 중앙 정렬 적용 */
}

.divider {
  transform: translateY(50px); /* 아이콘을 50px 아래로 이동 */
  width: 100%;
  border: 0;
  border-top: 1px solid #a3b9a8;
  margin: 20px 0;
}

#info_section {
  transform: translateY(60px); /* 아이콘을 60px 아래로 이동 */
  padding: 15px; /* 섹션 여백 추가 */
  text-align: justify; /* 텍스트를 양쪽 정렬로 설정 */
  font-size: 14px; /* 텍스트 크기를 약간 키움 */
  line-height: 1.3; /* 줄 간격을 넓혀 가독성 향상 */
  font-family: 'Noto Sans', Arial, sans-serif; /* 깔끔한 글꼴 설정 */
  color: #444; /* 부드러운 색상 */
  background-color: #f8f9fa; /* 약간의 배경색 추가 */
  border-radius: 8px; /* 둥근 모서리 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
  margin-top: 10px;
  margin-bottom: 40px;
}

#weather_section {
  transform: translateY(50px); /* 아이콘을 50px 아래로 이동 */
  padding: 10px;
  text-align: center; /* 텍스트와 아이콘을 중앙 정렬 */
  font-size: 16px;
  color: #333;
}

#weather_icon img {
  margin-top: 10px; /* 텍스트와 아이콘 사이 여백 */
  margin: 0 auto 15px auto; /* 위, 양옆 중앙 정렬 */
  width: 70px; /* 아이콘 너비 */
  height: 70px; /* 아이콘 높이 */
}

/* About Green Cane 섹션 */
#about_section {
  text-align: left;
  background-color: #4e684f; /* 연한 초록색 배경 */
  padding: 10px 0; /* 상하 여백 */
  border-bottom: 2px solid #a8c1ae; /* 아래쪽 테두리 */
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
  color: #f3fdf1; /* 텍스트 색상 */
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
  border-left: 2px solid #a8c1ae; /* 왼쪽 테두리 */
  box-shadow: -2px 0px 5px rgba(0, 0, 0, 0.1); /* 왼쪽 그림자 */
  height: calc(100vh - 120px); /* 상단 섹션을 제외한 화면 높이 */
  position: absolute; /* 위치를 고정 */
  right: 0; /* 오른쪽 끝에 붙임 */
  top: 110px; /* Green cane management application + About Green Cane의 높이 */

}

.icon {
  width: 70px;
  height: 70px;
  margin: 1px 0; /* 위아래 여백 최소화 */
  transition: all 0.3s ease-in-out; /* 크기 변화에 부드러운 전환 효과 */
}

.info_box {
  background-color: #f8f9fa; /* 박스 배경색 */
  border: 1px solid #c3e6cb; /* 테두리 */
  border-radius: 8px; /* 둥근 모서리 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
  width: 100%; /* 박스 너비 */
  height: 25px; /* 박스 높이 */
  margin: 3px 0; /* 위아래 여백 최소화 */
  display: flex; /* 박스를 flex로 설정 */
  justify-content: center; /* 중앙 정렬 */
  align-items: center; /* 중앙 정렬 */
  transition: all 0.3s ease-in-out; /* 부드러운 전환 효과 */
}

@media (max-width: 768px) {
  .info_box {
    width: 80%; /* 작은 화면에서는 박스 크기 80%로 설정 */
  }
}

/* 더 작은 화면에서 박스 크기 추가 축소 */
@media (max-width: 480px) {
  .info_box {
    width: 70%; /* 매우 작은 화면에서는 박스 크기 70%로 설정 */
  }
}


/* 섹션별 스타일링 */
#gps_info, #battery_info, #impact_info, #sound_info {
  width: 70%;
  margin-bottom: 10px;
  text-align: center;
}

#gps_info h3, #battery_info h3, #impact_info h3, #sound_info h3 {
  font-size: 18px;
  margin-bottom: 5px;
  text-align: left; /* 텍스트를 왼쪽 정렬 */
}

</style>
