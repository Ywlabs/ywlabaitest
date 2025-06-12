<template>
  <div class="energy-trend-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>에너지 트렌드 분석</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="trend-container">
      <div class="chart-wrapper">
        <canvas ref="globalChart"></canvas>
      </div>
      <div class="chart-wrapper">
        <canvas ref="domesticChart"></canvas>
      </div>
      <div class="chart-wrapper">
        <canvas ref="renewableChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'EnergyTrendWidget',
  setup() {
    const isLoading = ref(false)
    const globalChart = ref(null)
    const domesticChart = ref(null)
    const renewableChart = ref(null)
    const charts = ref([])

    // 샘플 데이터 생성
    const generateData = () => {
      const years = ['2018', '2019', '2020', '2021', '2022', '2023']
      return {
        global: {
          labels: years,
          datasets: [
            {
              label: '전 세계 에너지 소비 (EJ)',
              data: [580, 590, 570, 600, 620, 640],
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.4
            }
          ]
        },
        domestic: {
          labels: years,
          datasets: [
            {
              label: '국내 에너지 소비 (MTOE)',
              data: [280, 290, 285, 300, 310, 320],
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              tension: 0.4
            }
          ]
        },
        renewable: {
          labels: years,
          datasets: [
            {
              label: '신재생에너지 비율 (%)',
              data: [8, 10, 12, 15, 18, 20],
              borderColor: '#FFC107',
              backgroundColor: 'rgba(255, 193, 7, 0.1)',
              tension: 0.4
            }
          ]
        }
      }
    }

    // 차트 초기화
    const initCharts = () => {
      const data = generateData()
      
      // 전 세계 에너지 소비 추이 차트
      if (globalChart.value) {
        const ctx = globalChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'line',
          data: data.global,
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
                grid: {
                  color: 'rgba(0, 0, 0, 0.1)'
                }
              },
              x: {
                grid: {
                  display: false
                }
              }
            }
          }
        }))
      }

      // 국내 에너지 소비 추이 차트
      if (domesticChart.value) {
        const ctx = domesticChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'line',
          data: data.domestic,
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
                grid: {
                  color: 'rgba(0, 0, 0, 0.1)'
                }
              },
              x: {
                grid: {
                  display: false
                }
              }
            }
          }
        }))
      }

      // 신재생에너지 보급률 차트
      if (renewableChart.value) {
        const ctx = renewableChart.value.getContext('2d')
        charts.value.push(new Chart(ctx, {
          type: 'line',
          data: data.renewable,
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
                grid: {
                  color: 'rgba(0, 0, 0, 0.1)'
                }
              },
              x: {
                grid: {
                  display: false
                }
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
          if (index === 0) chart.data = data.global
          else if (index === 1) chart.data = data.domestic
          else if (index === 2) chart.data = data.renewable
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
      globalChart,
      domesticChart,
      renewableChart,
      isLoading,
      refreshData
    }
  }
}
</script>

<style scoped>
.energy-trend-widget {
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

.trend-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  overflow: auto;
  min-height: 0;
}

.trend-content {
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
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
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