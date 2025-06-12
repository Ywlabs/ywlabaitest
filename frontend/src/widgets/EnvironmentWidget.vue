<template>
  <div class="environment-widget-box">
    <div class="env-header">
      <span class="env-title">오늘의 회사 환경정보</span>
      <button class="refresh-btn" @click="fetchWeatherAndAir" :disabled="loading" title="새로고침">
        <svg class="refresh-icon" :class="{ spinning: loading }" viewBox="0 0 24 24" width="22" height="22">
          <path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6h-2c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" fill="#2355d6"/>
        </svg>
      </button>
    </div>
    <div v-if="loading" class="env-loading">
      <span class="spinner"></span>
      정보 불러오는 중...
    </div>
    <div v-else-if="error" class="env-error">{{ error }}</div>
    <div v-else :class="['weather-info', { 'loading-anim': loading }]">
      <div class="weather-main">
        <img :src="weatherIconUrl" :alt="weatherDesc" class="weather-icon" style="width:90px;height:90px;" />
        <div class="weather-desc">
          <span class="temp">{{ weather.temp }}℃</span>
          <span class="desc">{{ weatherDesc }}</span>
        </div>
      </div>
      <div class="air-quality">
        <div class="aqi-item">
          <span class="label">미세먼지(PM10)</span>
          <span :class="aqiClass(pm10)">{{ pm10 }} ㎍/㎥ ({{ pm10Grade }})</span>
        </div>
        <div class="aqi-item">
          <span class="label">초미세먼지(PM2.5)</span>
          <span :class="aqiClass(pm25)">{{ pm25 }} ㎍/㎥ ({{ pm25Grade }})</span>
        </div>
        <div class="aqi-item">
          <span class="label">통합대기환경지수</span>
          <span>{{ khai_grade || '-' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/common/axios'

// 날씨 아이콘 매핑 (OpenWeatherMap 기준)
const weatherIconMap = {
  'Clear': 'https://openweathermap.org/img/wn/01d.png',
  'Clouds': 'https://openweathermap.org/img/wn/03d.png',
  'Rain': 'https://openweathermap.org/img/wn/09d.png',
  'Drizzle': 'https://openweathermap.org/img/wn/09d.png',
  'Thunderstorm': 'https://openweathermap.org/img/wn/11d.png',
  'Snow': 'https://openweathermap.org/img/wn/13d.png',
  'Mist': 'https://openweathermap.org/img/wn/50d.png',
  'Smoke': 'https://openweathermap.org/img/wn/50d.png',
  'Haze': 'https://openweathermap.org/img/wn/50d.png',
  'Dust': 'https://openweathermap.org/img/wn/50d.png',
  'Fog': 'https://openweathermap.org/img/wn/50d.png',
  'Sand': 'https://openweathermap.org/img/wn/50d.png',
  'Ash': 'https://openweathermap.org/img/wn/50d.png',
  'Squall': 'https://openweathermap.org/img/wn/50d.png',
  'Tornado': 'https://openweathermap.org/img/wn/50d.png',
}

export default {
  name: 'EnvironmentWidget',
  data() {
    return {
      loading: true,
      error: null,
      weather: {
        temp: null,
        main: '',
        desc: ''
      },
      pm10: null,
      pm25: null,
      khai_grade: null,
    }
  },
  computed: {
    weatherIconUrl() {
      return weatherIconMap[this.weather.main] || weatherIconMap['Clear']
    },
    weatherDesc() {
      return this.weather.desc || this.weather.main
    },
    pm10Grade() {
      if (this.pm10 === null) return '-'
      if (this.pm10 <= 30) return '좋음'
      if (this.pm10 <= 80) return '보통'
      if (this.pm10 <= 150) return '나쁨'
      return '매우나쁨'
    },
    pm25Grade() {
      if (this.pm25 === null) return '-'
      if (this.pm25 <= 15) return '좋음'
      if (this.pm25 <= 35) return '보통'
      if (this.pm25 <= 75) return '나쁨'
      return '매우나쁨'
    },
    o3Grade() {
      return '-';
    }
  },
  methods: {
    aqiClass(val) {
      if (val === null) return 'aqi-good'
      if (typeof val === 'number') {
        if (val <= 30 || val <= 15 || val <= 0.030) return 'aqi-good'
        if (val <= 80 || val <= 35 || val <= 0.090) return 'aqi-moderate'
        if (val <= 150 || val <= 75 || val <= 0.150) return 'aqi-bad'
        return 'aqi-verybad'
      }
      return 'aqi-good'
    },
    async fetchWeatherAndAir() {
      this.loading = true; // 클릭 시 즉시 로딩 시작
      try {
        // 1. 백엔드에서 날씨 정보 받아오기
        const weatherRes = await api.get('/api/legacy/weather')
        if (weatherRes.data.status === 'success') {
          this.weather.temp = Math.round(weatherRes.data.data.temp)
          this.weather.main = weatherRes.data.data.main
          this.weather.desc = weatherRes.data.data.desc
        } else {
          throw new Error(weatherRes.data.message || '날씨 정보 오류')
        }
        // 2. 백엔드에서 대기질 정보 받아오기
        const airRes = await api.get('/api/legacy/air-quality')
        if (airRes.data.status === 'success') {
          // API는 문자열로 반환하므로 숫자로 변환
          this.pm10 = airRes.data.data.pm10 ? Number(airRes.data.data.pm10) : null
          this.pm25 = airRes.data.data.pm25 ? Number(airRes.data.data.pm25) : null
          this.khai_grade = airRes.data.data.khai_grade || null;
        } else {
          throw new Error(airRes.data.message || '대기질 정보 오류')
        }
      } catch (e) {
        this.error = '날씨/대기질 정보를 불러오지 못했습니다.'
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.fetchWeatherAndAir();
    this._interval = setInterval(() => {
      this.fetchWeatherAndAir();
    }, 12 * 60 * 1000); // 12분마다 갱신
  },
  beforeUnmount() {
    if (this._interval) clearInterval(this._interval);
  },
}
</script>

<style scoped>
.environment-widget-box {
  padding: 20px;
  background: #f4f8fb;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  text-align: center;
  position: relative;
  min-width: 320px;
  max-width: 420px;
  margin: 0 auto;
  font-size: 1.08em;
}
.env-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.env-title {
  font-size: 1.08em;
  color: #666;
  font-weight: bold;
}
.refresh-btn {
  background: transparent;
  border: none;
  font-size: 1.2em;
  color: #2355d6;
  cursor: pointer;
  padding: 2px 2px 2px 8px;
  border-radius: 50%;
  transition: background 0.15s, color 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.refresh-btn:disabled {
  color: #bbb;
  cursor: not-allowed;
}
.refresh-icon {
  transition: transform 0.2s;
  width: 22px;
  height: 22px;
  display: block;
}
.spinning {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.env-loading, .env-error {
  color: #d32f2f;
  margin: 18px 0 12px 0;
  text-align: center;
}
.weather-main {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
  justify-content: center;
}
.weather-icon {
  width: 90px;
  height: 90px;
}
.weather-desc {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-start;
}
.temp {
  font-size: 2rem;
  font-weight: 600;
  color: #2355d6;
}
.desc {
  font-size: 1.1rem;
  color: #333;
}
.air-quality {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.aqi-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
}
.label {
  color: #888;
  font-weight: 500;
}
.aqi-good {
  color: #409eff;
}
.aqi-moderate {
  color: #e6a23c;
}
.aqi-bad {
  color: #d32f2f;
}
.aqi-verybad {
  color: #b71c1c;
}
.weather-info {
  transition: opacity 0.4s, filter 0.4s;
}
.loading-anim {
  opacity: 0.5;
  filter: blur(2px);
  pointer-events: none;
}
.env-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333; /* 진한 회색 */
  font-weight: 500;
  font-size: 1.05em;
  margin: 18px 0 16px 0;
  min-height: 32px;
  gap: 10px;
}
.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid #42b983;
  border-top: 3px solid #e0e0e0;
  border-radius: 50%;
  margin-right: 8px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 