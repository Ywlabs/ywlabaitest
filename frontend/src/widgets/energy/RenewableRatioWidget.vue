<template>
  <div class="renewable-ratio-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>신재생에너지 비율</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>
    <div class="ratio-container">
      <div class="energy-sources">
        <div class="source-item" v-for="(source, index) in energySources" :key="index">
          <div class="source-header">
            <span class="name">{{ source.name }}</span>
            <span class="ratio">{{ source.ratio }}%</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress" 
              :style="{ width: `${source.ratio}%`, backgroundColor: source.color }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'RenewableRatioWidget',
  setup() {
    const isLoading = ref(false)
    const renewableRatio = ref(0)
    const energySources = ref([])

    // 목표 달성 상태 계산
    const goalStatus = computed(() => {
      const ratio = renewableRatio.value
      if (ratio >= 100) return 'RE100 목표를 달성했습니다!'
      if (ratio >= 80) return 'RE100 목표 달성이 임박했습니다.'
      if (ratio >= 50) return 'RE100 목표 달성을 위해 노력하고 있습니다.'
      return 'RE100 목표 달성을 위해 더 많은 노력이 필요합니다.'
    })

    const goalStatusClass = computed(() => {
      const ratio = renewableRatio.value
      if (ratio >= 100) return 'achieved'
      if (ratio >= 80) return 'near'
      if (ratio >= 50) return 'progress'
      return 'need-effort'
    })

    // 샘플 데이터 생성
    const generateData = () => {
      const total = 100
      const sources = [
        { name: '태양광', ratio: 0, color: '#FFC107' },
        { name: '풍력', ratio: 0, color: '#2196F3' },
        { name: '수력', ratio: 0, color: '#4CAF50' },
        { name: '바이오매스', ratio: 0, color: '#795548' },
        { name: '기타', ratio: 0, color: '#9E9E9E' }
      ]

      // 각 에너지원의 비율 랜덤 생성
      let remaining = total
      sources.forEach((source, index) => {
        if (index === sources.length - 1) {
          source.ratio = remaining
        } else {
          source.ratio = Math.floor(Math.random() * (remaining / 2))
          remaining -= source.ratio
        }
      })

      // 전체 신재생에너지 비율 계산
      renewableRatio.value = Math.floor(Math.random() * 40) + 60

      return sources
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        energySources.value = generateData()
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      energySources.value = generateData()
    })

    return {
      renewableRatio,
      energySources,
      goalStatus,
      goalStatusClass,
      isLoading,
      refreshData
    }
  }
}
</script>

<style scoped>
.renewable-ratio-widget {
  background: white;
  border-radius: 12px;
  padding: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

.widget-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}

.widget-header h3 {
  margin: 0;
  font-size: 1.08rem;
  color: #333;
}

.refresh-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
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

.ratio-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.energy-sources {
  width: 100%;
  max-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.source-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.source-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.name {
  font-size: 0.85rem;
  color: #666;
}

.ratio {
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
}

.progress-bar {
  height: 5px;
  background: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  transition: width 0.3s ease;
}

.goal-status {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  margin-top: 20px;
}

.goal-status h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  color: #333;
}

.goal-status p {
  margin: 0;
  font-size: 0.9rem;
}

.goal-status.achieved {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.goal-status.near {
  background-color: #fff3e0;
  color: #ef6c00;
}

.goal-status.progress {
  background-color: #e3f2fd;
  color: #1565c0;
}

.goal-status.need-effort {
  background-color: #ffebee;
  color: #c62828;
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