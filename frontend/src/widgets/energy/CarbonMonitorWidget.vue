<template>
  <div class="carbon-monitor-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>탄소배출량 모니터링</h3>
      <button class="refresh-btn">↻</button>
    </div>
    
    <div class="chart-container">
      <canvas ref="carbonChart"></canvas>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'CarbonMonitorWidget',
  setup() {
    const carbonChart = ref(null)
    const chart = ref(null)
    const isLoading = ref(false)

    // 샘플 데이터 생성
    const generateData = () => {
      const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
      return {
        labels: months,
        datasets: [
          {
            label: '탄소배출량 (톤)',
            data: months.map(() => Math.floor(Math.random() * 1000) + 500),
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      }
    }

    // 차트 초기화
    const initChart = () => {
      if (carbonChart.value) {
        const ctx = carbonChart.value.getContext('2d')
        chart.value = new Chart(ctx, {
          type: 'line',
          data: generateData(),
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#4CAF50',
                borderWidth: 1
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
            },
            animation: {
              duration: 1000,
              easing: 'easeInOutQuart'
            }
          }
        })
      }
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        // 실제 구현시에는 API 호출로 대체
        await new Promise(resolve => setTimeout(resolve, 1000))
        chart.value.data = generateData()
        chart.value.update()
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
      carbonChart,
      isLoading,
      refreshData
    }
  }
}
</script>

<style scoped>
.carbon-monitor-widget {
  background: white;
  border-radius: 12px;
  padding: 20px;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto;
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

.chart-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: auto;
  min-height: 0;
}

.chart-container canvas {
  flex: 1;
  min-height: 0;
  max-height: 200px;
}

.close-btn {
  position: absolute;
  top: 16px;
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