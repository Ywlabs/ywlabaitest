<template>
  <div class="energy-alert-widget">
    <button class="close-btn" @click="$emit('close')">×</button>
    <div class="widget-header">
      <h3>에너지 알림</h3>
      <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
        <span v-if="isLoading" class="loading-spinner"></span>
        <span v-else>↻</span>
      </button>
    </div>

    <div class="alert-container">
      <div class="alert-card critical">
        <div class="alert-icon">❗</div>
        <div class="alert-label">CRITICAL</div>
        <div class="alert-count">{{ alerts.critical.count }}</div>
      </div>

      <div class="alert-card major">
        <div class="alert-icon">⚠️</div>
        <div class="alert-label">MAJOR</div>
        <div class="alert-count">{{ alerts.major.count }}</div>
      </div>

      <div class="alert-card minor">
        <div class="alert-icon">ℹ️</div>
        <div class="alert-label">MINOR</div>
        <div class="alert-count">{{ alerts.minor.count }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'EnergyAlertWidget',
  setup() {
    const isLoading = ref(false)
    const alerts = ref({
      critical: {
        count: 0,
        items: []
      },
      major: {
        count: 0,
        items: []
      },
      minor: {
        count: 0,
        items: []
      }
    })

    // 샘플 알림 데이터 생성
    const generateAlerts = () => {
      const criticalItems = [
        '전력 공급 중단 위험',
        '고온 경보 발생',
        '비상 정전 발생'
      ]
      const majorItems = [
        '전력 사용량 급증',
        '설비 과부하 경고',
        '배전반 이상 감지'
      ]
      const minorItems = [
        '일시적 전압 불안정',
        '설비 점검 필요',
        '일반 경고 발생'
      ]

      return {
        critical: {
          count: Math.floor(Math.random() * 3),
          items: criticalItems.slice(0, Math.floor(Math.random() * 3) + 1)
        },
        major: {
          count: Math.floor(Math.random() * 4),
          items: majorItems.slice(0, Math.floor(Math.random() * 4) + 1)
        },
        minor: {
          count: Math.floor(Math.random() * 5),
          items: minorItems.slice(0, Math.floor(Math.random() * 5) + 1)
        }
      }
    }

    // 데이터 새로고침
    const refreshData = async () => {
      isLoading.value = true
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        alerts.value = generateAlerts()
      } finally {
        isLoading.value = false
      }
    }

    // 1분마다 데이터 갱신
    let timer
    onMounted(() => {
      refreshData()
      timer = setInterval(refreshData, 60000)
    })

    onUnmounted(() => {
      if (timer) {
        clearInterval(timer)
      }
    })

    return {
      alerts,
      isLoading,
      refreshData
    }
  }
}
</script>

<style scoped>
.energy-alert-widget {
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

.alert-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: stretch;
  margin-top: 8px;
  padding: 12px 0;
}

.alert-card {
  flex: none;
  max-width: 200px;
  min-width: 0;
  margin: 0 auto;
  border-radius: 16px;
  padding: 24px 18px 18px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 2px solid transparent;
}

.alert-card.critical {
  background: #ffeaea;
  border-color: #ffb3b3;
  color: #c62828;
}

.alert-card.major {
  background: #fffbe6;
  border-color: #ffe082;
  color: #b8860b;
}

.alert-card.minor {
  background: #e3f2fd;
  border-color: #90caf9;
  color: #1976d2;
}

.alert-icon {
  font-size: 1.7em;
  margin-bottom: 6px;
}

.alert-label {
  font-size: 1em;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
  text-transform: uppercase;
}

.alert-count {
  font-size: 1.7em;
  font-weight: 700;
  line-height: 1.1;
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