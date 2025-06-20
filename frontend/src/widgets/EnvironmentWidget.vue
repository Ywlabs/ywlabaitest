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
    <CommonLoading v-if="loading" message="환경 정보를 불러오는 중..." />
    <CommonError v-else-if="error" :message="error" @retry="fetchWeatherAndAir" />
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
      <div class="update-time">
        마지막 업데이트: {{ lastUpdateTime }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import api from '@/common/axios'
import CommonLoading from '@/components/CommonLoading.vue'
import CommonError from '@/components/CommonError.vue'

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
  components: { CommonLoading, CommonError },
  setup() {
    const loading = ref(true)
    const error = ref(null)
    const weather = ref({
      temp: null,
      main: '',
      desc: ''
    })
    const pm10 = ref(null)
    const pm25 = ref(null)
    const khai_grade = ref(null)
    const eventSource = ref(null)
    const lastUpdateTime = ref(null)
    let pollingInterval = null

    const weatherIconUrl = computed(() => {
      return weatherIconMap[weather.value.main] || weatherIconMap['Clear']
    })

    const weatherDesc = computed(() => {
      return weather.value.desc || weather.value.main
    })

    const pm10Grade = computed(() => {
      if (pm10.value === null) return '-'
      if (pm10.value <= 30) return '좋음'
      if (pm10.value <= 80) return '보통'
      if (pm10.value <= 150) return '나쁨'
      return '매우나쁨'
    })

    const pm25Grade = computed(() => {
      if (pm25.value === null) return '-'
      if (pm25.value <= 15) return '좋음'
      if (pm25.value <= 35) return '보통'
      if (pm25.value <= 75) return '나쁨'
      return '매우나쁨'
    })

    const aqiClass = (val) => {
      if (val === null) return 'aqi-good'
      if (typeof val === 'number') {
        if (val <= 30 || val <= 15 || val <= 0.030) return 'aqi-good'
        if (val <= 80 || val <= 35 || val <= 0.090) return 'aqi-moderate'
        if (val <= 150 || val <= 75 || val <= 0.150) return 'aqi-bad'
        return 'aqi-verybad'
      }
      return 'aqi-good'
    }

    const setupSSE = () => {
      // 기존 EventSource가 있다면 닫기
      if (eventSource.value) {
        eventSource.value.close()
      }

      // 새로운 EventSource 연결
      eventSource.value = new EventSource('http://localhost:5000/api/environment/stream')

      // SSE 이벤트 리스너 설정
      eventSource.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'ping') {
            return // ping 메시지는 무시
          }
          if (data.status === 'success') {
            updateEnvironmentData(data.data)
            error.value = null // 성공 시 에러 메시지 제거
          } else if (data.status === 'error') {
            error.value = data.message
          }
        } catch (e) {
          console.error('SSE 데이터 파싱 오류:', e)
          error.value = '데이터 처리 중 오류가 발생했습니다.'
        }
      }

      eventSource.value.onerror = (error) => {
        console.error('SSE 연결 오류:', error)
        error.value = '실시간 업데이트 연결이 끊어졌습니다.'
        // SSE 연결 실패 시 폴링으로 폴백
        eventSource.value.close()
        startPolling()
      }
    }

    const startPolling = () => {
      // 1분마다 폴링
      if (pollingInterval) {
        clearInterval(pollingInterval)
      }
      pollingInterval = setInterval(() => {
        fetchWeatherAndAir()
      }, 60 * 1000)
    }

    const fetchWeatherAndAir = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/environment/current')
        if (response.data && response.data.success) {
          updateEnvironmentData(response.data.data)
          error.value = null // 성공 시 에러 메시지 제거
        } else {
          throw new Error(response.data.message || '환경 정보 조회에 실패했습니다.')
        }
      } catch (e) {
        error.value = '환경 정보를 불러오는 중 네트워크 오류가 발생했습니다.'
        console.error('환경 정보 조회 오류:', e)
      } finally {
        loading.value = false
      }
    }

    const updateEnvironmentData = (data) => {
      try {
        if (!data) {
          console.error('환경 정보 데이터가 없습니다.')
          error.value = '환경 정보를 가져올 수 없습니다.'
          return
        }

        // 날씨 정보 업데이트
        try {
          const weatherData = data.weather || {}
          weather.value.temp = weatherData.temp ? Math.round(Number(weatherData.temp)) : 0
          weather.value.main = weatherData.main || ''
          weather.value.desc = weatherData.weather_desc || weatherData.description || ''
        } catch (e) {
          console.error('날씨 정보 업데이트 실패:', e)
          weather.value.temp = 0
          weather.value.main = ''
          weather.value.desc = ''
        }
        
        // 대기질 정보 업데이트
        try {
          const airQualityData = data.air_quality || {}
          pm10.value = airQualityData.pm10 ? Number(airQualityData.pm10) : 0
          pm25.value = airQualityData.pm25 ? Number(airQualityData.pm25) : 0
          khai_grade.value = airQualityData.khai_grade || ''
        } catch (e) {
          console.error('대기질 정보 업데이트 실패:', e)
          pm10.value = 0
          pm25.value = 0
          khai_grade.value = ''
        }
        
        // 타임스탬프 업데이트
        try {
          if (data.timestamp) {
            const date = new Date(data.timestamp)
            if (!isNaN(date.getTime())) {
              lastUpdateTime.value = date.toLocaleString('ko-KR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
              })
            } else {
              lastUpdateTime.value = '날짜 정보 없음'
            }
          } else {
            lastUpdateTime.value = '날짜 정보 없음'
          }
        } catch (e) {
          console.error('타임스탬프 업데이트 실패:', e)
          lastUpdateTime.value = '날짜 정보 없음'
        }
        
        console.info('환경 정보 업데이트 완료:', {
          temp: weather.value.temp,
          main: weather.value.main,
          desc: weather.value.desc,
          pm10: pm10.value,
          pm25: pm25.value,
          khai_grade: khai_grade.value,
          timestamp: lastUpdateTime.value
        })
      } catch (error) {
        console.error('환경 정보 업데이트 중 오류:', error)
        error.value = '데이터 처리 중 오류가 발생했습니다.'
      }
    }

    onMounted(() => {
      // 초기 데이터 로드
      fetchWeatherAndAir()
      
      // SSE 연결 시도
      setupSSE()
    })

    onUnmounted(() => {
      // 컴포넌트 언마운트 시 정리
      if (eventSource.value) {
        eventSource.value.close()
      }
      if (pollingInterval) {
        clearInterval(pollingInterval)
      }
    })

    return {
      loading,
      error,
      weather,
      pm10,
      pm25,
      khai_grade,
      lastUpdateTime,
      weatherIconUrl,
      weatherDesc,
      pm10Grade,
      pm25Grade,
      aqiClass,
      fetchWeatherAndAir
    }
  }
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

/* 마지막 업데이트 시간 표시 스타일 추가 */
.update-time {
  font-size: 0.8em;
  color: #888;
  margin-top: 8px;
  text-align: right;
}
</style> 