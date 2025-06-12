<template>
  <div class="power-peak-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>전력 피크 예측</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="peak-container">
      <div class="chart-wrapper">
        <canvas ref="peakChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'PowerPeakWidget',
  setup() {
    const isLoading = ref(false)
    const peakChart = ref(null)
    const chart = ref(null)
    const peakTime = ref('')
    const peakValue = ref(0)
    const gridImpact = ref('')
    const impactDescription = ref('')

    // 숫자 포맷팅
    const formatNumber = (num) => {
      return new Intl.NumberFormat('ko-KR').format(Math.round(num))
    }

    // 그리드 영향도에 따른 클래스
    const gridImpactClass = computed(() => {
      const impact = gridImpact.value.toLowerCase()
      if (impact.includes('높음')) return 'high'
      if (impact.includes('중간')) return 'medium'
      return 'low'
    })

    // 샘플 데이터 생성
    const generateData = () => {
      const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`)
      const baseLoad = 1000
      const peakLoad = baseLoad + Math.random() * 500
      const data = hours.map(hour => {
        const hourNum = parseInt(hour)
        // 피크 시간대 (14:00-16:00)에 높은 부하
        if (hourNum >= 14 && hourNum <= 16) {
          return peakLoad - Math.random() * 100
        }
        // 일반 시간대
        return baseLoad + Math.random() * 200
      })

      // 피크 시간과 값 찾기
      const maxIndex = data.indexOf(Math.max(...data))
      peakTime.value = hours[maxIndex]
      peakValue.value = data[maxIndex]

      // 그리드 영향도 설정
      const impact = Math.random()
      if (impact > 0.7) {
        gridImpact.value = '높음'
        impactDescription.value = '전력 공급에 주의가 필요합니다.'
      } else if (impact > 0.3) {
        gridImpact.value = '중간'
        impactDescription.value = '일반적인 전력 공급이 가능합니다.'
      } else {
        gridImpact.value = '낮음'
        impactDescription.value = '안정적인 전력 공급이 가능합니다.'
      }

      return {
        labels: hours,
        datasets: [{
          label: '전력 수요 (MW)',
          data: data,
          borderColor: '#2196F3',
          backgroundColor: 'rgba(33, 150, 243, 0.1)',
          tension: 0.4,
          fill: true
        }]
      }
    }

    // 차트 초기화
    const initChart = () => {
      if (peakChart.value) {
        const ctx = peakChart.value.getContext('2d')
        chart.value = new Chart(ctx, {
          type: 'line',
          data: generateData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: false,
                title: {
                  display: true,
                  text: 'MW'
                }
              }
            }
          }
        })
      }
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        const data = generateData()
        if (chart.value) {
          chart.value.data = data
          chart.value.update()
        }
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      initChart()
    })

    onUnmounted(() => {
      if (chart.value) {
        chart.value.destroy()
      }
    })

    return {
      peakChart,
      peakTime,
      peakValue,
      gridImpact,
      impactDescription,
      gridImpactClass,
      isLoading,
      refreshData,
      formatNumber
    }
  }
}
</script>

<style scoped>
.power-peak-widget {
  height: 100%;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  padding: 0;
  margin: 0;
  background: white;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  font-size: 13px;
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.widget-header h3 {
  margin: 0 0 2px 0;
  padding: 0;
  font-size: 15px;
  color: #333;
}

.refresh-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.refresh-btn:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.refresh-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.peak-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0;
  gap: 0;
}

.chart-wrapper {
  flex: 0 0 90%;
  min-height: 0;
  max-height: 90%;
  overflow: hidden;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
}

.chart-wrapper h4 {
  margin: 0 0 16px 0;
  font-size: 1rem;
  color: #333;
  text-align: center;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
  max-height: 100% !important;
  object-fit: contain;
  display: block;
}

.peak-info-row {
  display: flex;
  flex-direction: row;
  gap: 16px;
  justify-content: space-between;
  align-items: stretch;
  margin-top: 8px;
}

.info-card {
  flex: 1;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
}

.info-card h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: #333;
}

.peak-time {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2196F3;
  margin-bottom: 8px;
}

.peak-value {
  font-size: 1.2rem;
  color: #666;
}

.grid-impact {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.grid-impact.high {
  color: #f44336;
}

.grid-impact.medium {
  color: #ff9800;
}

.grid-impact.low {
  color: #4CAF50;
}

.impact-description {
  font-size: 0.9rem;
  color: #666;
}

.loading-spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.close-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 10;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 16px;
  line-height: 22px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: background 0.2s;
  padding: 0;
}

.close-btn:hover {
  background: #f5f5f5;
}

.peak-info h4, .peak-info strong, .peak-info span {
  font-size: 13px !important;
  margin: 0;
  padding: 0;
}
</style> 