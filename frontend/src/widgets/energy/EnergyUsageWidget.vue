<template>
  <div class="energy-usage-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>에너지 소비 현황</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="usage-container">
      <div class="chart-wrapper">
        <canvas ref="usageChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'EnergyUsageWidget',
  setup() {
    const isLoading = ref(false)
    const usageChart = ref(null)
    const chart = ref(null)
    const energyData = ref({
      coal: 0,
      oil: 0,
      gas: 0,
      nuclear: 0,
      renewable: 0
    })

    // 에너지 데이터 요약
    const energySummary = computed(() => [
      { label: '석탄', value: energyData.value.coal, color: '#795548' },
      { label: '석유', value: energyData.value.oil, color: '#607D8B' },
      { label: '천연가스', value: energyData.value.gas, color: '#2196F3' },
      { label: '원자력', value: energyData.value.nuclear, color: '#FFC107' },
      { label: '신재생에너지', value: energyData.value.renewable, color: '#4CAF50' }
    ])

    // 총 에너지 소비량
    const totalEnergy = computed(() => {
      return Object.values(energyData.value).reduce((sum, value) => sum + value, 0)
    })

    // 숫자 포맷팅
    const formatNumber = (num) => {
      return new Intl.NumberFormat('ko-KR').format(Math.round(num))
    }

    // 샘플 데이터 생성
    const generateData = () => {
      return {
        coal: Math.random() * 1000 + 500,
        oil: Math.random() * 2000 + 1000,
        gas: Math.random() * 1500 + 800,
        nuclear: Math.random() * 800 + 400,
        renewable: Math.random() * 600 + 300
      }
    }

    // 차트 초기화
    const initChart = () => {
      if (usageChart.value) {
        const ctx = usageChart.value.getContext('2d')
        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['석탄', '석유', '천연가스', '원자력', '신재생에너지'],
            datasets: [{
              data: Object.values(energyData.value),
              backgroundColor: [
                '#795548',
                '#607D8B',
                '#2196F3',
                '#FFC107',
                '#4CAF50'
              ]
            }]
          },
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
                  text: 'TOE'
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
        energyData.value = generateData()
        if (chart.value) {
          chart.value.data.datasets[0].data = Object.values(energyData.value)
          chart.value.update()
        }
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      energyData.value = generateData()
      initChart()
    })

    onUnmounted(() => {
      if (chart.value) {
        chart.value.destroy()
      }
    })

    return {
      usageChart,
      energySummary,
      totalEnergy,
      isLoading,
      refreshData,
      formatNumber
    }
  }
}
</script>

<style scoped>
.energy-usage-widget {
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

.usage-container {
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
  flex: 1;
  min-height: 0;
  max-height: 200px;
}

.summary-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: auto;
  min-height: 0;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  font-size: 0.9rem;
  color: #666;
}

.value {
  font-size: 1rem;
  font-weight: 500;
  color: #333;
}

.progress-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  transition: width 0.3s ease;
}

.percentage {
  font-size: 0.8rem;
  color: #666;
  text-align: right;
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