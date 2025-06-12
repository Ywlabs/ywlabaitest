<template>
  <div class="energy-cost-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>에너지 비용 분석</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="cost-container">
      <div class="chart-wrapper">
        <canvas ref="energyTypeChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'EnergyCostWidget',
  setup() {
    const isLoading = ref(false)
    const energyTypeChart = ref(null)
    const regionChart = ref(null)
    const industryChart = ref(null)
    const charts = ref([])

    // 샘플 데이터 생성
    const generateData = () => {
      return {
        energyType: {
          labels: ['전기', '가스', '수도', '열에너지'],
          datasets: [{
            data: [45, 25, 15, 15],
            backgroundColor: ['#4CAF50', '#2196F3', '#00BCD4', '#FFC107']
          }]
        },
        region: {
          labels: ['서울', '부산', '인천', '대구', '광주'],
          datasets: [{
            label: '에너지 소비량 (MWh)',
            data: [1200, 800, 600, 900, 700],
            backgroundColor: 'rgba(33, 150, 243, 0.5)',
            borderColor: '#2196F3',
            borderWidth: 1
          }]
        },
        industry: {
          labels: ['제조업', '건설업', '서비스업', 'IT', '기타'],
          datasets: [{
            label: '에너지 사용량 (GWh)',
            data: [2500, 1500, 2000, 1800, 1200],
            backgroundColor: 'rgba(76, 175, 80, 0.5)',
            borderColor: '#4CAF50',
            borderWidth: 1
          }]
        }
      }
    }

    // 차트 초기화
    const initCharts = () => {
      const data = generateData()
      
      // 에너지 종류별 비용 차트
      if (energyTypeChart.value) {
        const ctx = energyTypeChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'doughnut',
          data: data.energyType,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        }))
      }

      // 지역별 소비 현황 차트
      if (regionChart.value) {
        const ctx = regionChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'bar',
          data: data.region,
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
                beginAtZero: true
              }
            }
          }
        }))
      }

      // 산업별 사용량 차트
      if (industryChart.value) {
        const ctx = industryChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'bar',
          data: data.industry,
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
                beginAtZero: true
              }
            }
          }
        }))
      }
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        const data = generateData()
        charts.value.forEach((chart, index) => {
          if (index === 0) chart.data = data.energyType
          else if (index === 1) chart.data = data.region
          else if (index === 2) chart.data = data.industry
          chart.update()
        })
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      initCharts()
    })

    onUnmounted(() => {
      charts.value.forEach(chart => chart.destroy())
    })

    return {
      energyTypeChart,
      regionChart,
      industryChart,
      isLoading,
      refreshData
    }
  }
}
</script>

<style scoped>
.energy-cost-widget {
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
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.widget-header h3 {
  margin: 0;
  font-size: 1.2rem;
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

.cost-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  flex: 1;
  min-height: 0;
  max-height: 200px;
  overflow: hidden;
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
  min-height: 0;
}

.cost-list {
  flex: 1;
  min-height: 0;
  overflow: hidden;
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
</style> 