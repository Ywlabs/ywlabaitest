<template>
  <div class="facility-energy-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>설비별 에너지 사용량</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="facility-container">
      <div class="chart-wrapper">
        <canvas ref="facilityChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'FacilityEnergyWidget',
  setup() {
    const isLoading = ref(false)
    const facilityChart = ref(null)
    const chart = ref(null)
    const facilityData = ref([])

    // 숫자 포맷팅
    const formatNumber = (num) => {
      return new Intl.NumberFormat('ko-KR').format(Math.round(num))
    }

    // 샘플 데이터 생성
    const generateData = () => {
      const facilities = [
        { name: '보일러', usage: 0, efficiency: 0, status: '' },
        { name: '냉동기', usage: 0, efficiency: 0, status: '' },
        { name: '공조기', usage: 0, efficiency: 0, status: '' },
        { name: '펌프', usage: 0, efficiency: 0, status: '' },
        { name: '전기실', usage: 0, efficiency: 0, status: '' }
      ]

      return facilities.map(facility => ({
        ...facility,
        usage: Math.random() * 1000 + 500,
        efficiency: Math.floor(Math.random() * 40) + 60,
        status: Math.random() > 0.8 ? '점검 필요' : '정상'
      }))
    }

    // 차트 초기화
    const initChart = () => {
      if (facilityChart.value) {
        const ctx = facilityChart.value.getContext('2d')
        const data = {
            labels: facilityData.value.map(f => f.name),
            datasets: [{
              label: '에너지 사용량 (kWh)',
              data: facilityData.value.map(f => f.usage),
              backgroundColor: facilityData.value.map(f => 
                f.efficiency >= 80 ? '#4CAF50' : f.efficiency < 60 ? '#f44336' : '#2196F3'
              )
            }]
        }

        chart.value = new Chart(ctx, {
          type: 'bar',
          data: data,
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
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'kWh'
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
        facilityData.value = generateData()
        if (chart.value) {
          const newData = {
            labels: facilityData.value.map(f => f.name),
            datasets: [{
              label: '에너지 사용량 (kWh)',
              data: facilityData.value.map(f => f.usage),
              backgroundColor: facilityData.value.map(f => 
            f.efficiency >= 80 ? '#4CAF50' : f.efficiency < 60 ? '#f44336' : '#2196F3'
          )
            }]
          }
          chart.value.data = newData
          chart.value.update()
        }
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      facilityData.value = generateData()
      nextTick(() => {
      initChart()
      })
    })

    onUnmounted(() => {
      if (chart.value) {
        chart.value.destroy()
      }
    })

    return {
      facilityChart,
      facilityData,
      isLoading,
      refreshData,
      formatNumber
    }
  }
}
</script>

<style scoped>
.facility-energy-widget {
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

.facility-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0;
  gap: 0;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
  max-height: 200px;
  overflow: hidden;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: center;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
  max-height: 100% !important;
  object-fit: contain;
  display: block;
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
</style> 