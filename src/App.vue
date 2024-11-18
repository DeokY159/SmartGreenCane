<template>
  <div>
  <header>
    <nav-bar id="nav" />
  </header>
  <div id="app">
    <div id="main_title">
      <h1>스마트 그린케인 어플리케이션에 오신 것을 환영합니다!</h1>
      <p>이곳에서 시각장애인의 위치 및 상태를 확인할 수 있습니다.</p>
    </div>
    <div id="map"></div>
  </div>
</div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import navBar from './components/navBar.vue';

export default {
  name: 'App',
  components: {
    navBar,
  },
  data() {
    return {
      userLocation: [37.5507583, 127.0741682], // 초기 사용자 좌표
      map: null, 
    };
  },
  methods: {
    updateLocation(lat, lng) {
      this.userLocation = [lat, lng];
      this.map.setView(this.userLocation, 16); // 지도 중심 이동
    },
  },
  mounted() {
    // 지도 생성
    this.map = L.map('map').setView(this.userLocation, 16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.map);

    // 초기 마커 생성
    const marker = L.marker(this.userLocation)
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
}

#map {
  height: 60vh;
  width: 60%;
  float: left;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  margin-left: 20%;
  margin-top: 50px;
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

#nav {
  margin-bottom: 15px;
  min-width: 1200px;
  overflow: hidden;
  margin-right: 0px;
}
</style>
