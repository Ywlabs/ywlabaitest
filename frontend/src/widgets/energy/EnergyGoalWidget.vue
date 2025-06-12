<template>
  <div class="energy-goal-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>에너지 목표 달성률</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="goal-container">
      <div class="progress-circle">
        <svg viewBox="0 0 36 36" class="circular-chart">
          <path
            class="circle-bg"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <path
            class="circle"
            :stroke-dasharray="`${achievementRate}, 100`"
            d="M18 2.0845
              a 15.9155 15.9155 0 0 1 0 31.831
              a 15.9155 15.9155 0 0 1 0 -31.831"
          />
          <text x="18" y="20.35" class="percentage">{{ achievementRate }}%</text>
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'EnergyGoalWidget',
  setup() {
    const isLoading = ref(false)
    const goal = ref(10000)
    const achieved = ref(0)
    const achievementRate = computed(() => Math.round((achieved.value / goal.value) * 100))

    // 가이드 메시지 및 스타일 결정
    const guideMessage = computed(() => {
      const rate = achievementRate.value
      if (rate >= 90) return '목표 달성이 임박했습니다!'
      if (rate >= 70) return '목표 달성을 위해 노력하고 있습니다.'
      if (rate >= 50) return '목표 달성을 위해 더 많은 노력이 필요합니다.'
      return '목표 달성을 위해 대책이 필요합니다.'
    })

    const messageClass = computed(() => {
      const rate = achievementRate.value
      if (rate >= 90) return 'success'
      if (rate >= 70) return 'warning'
      return 'danger'
    })

    // 숫자 포맷팅
    const formatNumber = (num) => {
      return new Intl.NumberFormat('ko-KR').format(num)
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        // 실제 구현시에는 API 호출로 대체
        achieved.value = Math.floor(Math.random() * goal.value)
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      refreshData()
    })

    return {
      goal,
      achieved,
      achievementRate,
      guideMessage,
      messageClass,
      isLoading,
      refreshData,
      formatNumber
    }
  }
}
</script>

<style scoped>
.energy-goal-widget {
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

.goal-content {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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

.goal-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  overflow: auto;
  min-height: 0;
}

.progress-circle {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
}

.circular-chart {
  display: block;
  margin: 0 auto;
  max-width: 100%;
}

.circle-bg {
  fill: none;
  stroke: #eee;
  stroke-width: 3;
}

.circle {
  fill: none;
  stroke-width: 3;
  stroke-linecap: round;
  animation: progress 1s ease-out forwards;
  stroke: #4CAF50;
}

.percentage {
  fill: #666;
  font-size: 0.5em;
  text-anchor: middle;
  font-weight: bold;
}

.guide-message {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  margin-top: 20px;
}

.guide-message.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.guide-message.warning {
  background-color: #fff3e0;
  color: #ef6c00;
}

.guide-message.danger {
  background-color: #ffebee;
  color: #c62828;
}

@keyframes progress {
  0% {
    stroke-dasharray: 0 100;
  }
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