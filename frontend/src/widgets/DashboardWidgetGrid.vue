<template>
  <div>
    <div class="dashboard-dim" @click="$emit('close')"></div>
    <div class="dashboard-widget-grid">
      <!-- 상단: 검색창/버튼/닫기 -->
      <div class="dashboard-header">
        <div class="search-container">
          <div class="search-area">
            <input 
              v-model="searchQuery" 
              placeholder="보고싶은 에너지데이터를 알려주세요?" 
              class="search-input" 
              @keyup.enter="handleSearch"
              :disabled="isLoading" 
              ref="searchInput"
            />
            <button 
              @click="handleSearch" 
              class="search-btn"
              :disabled="isLoading || !searchQuery.trim()"
            >
              <span v-if="isLoading" class="loading-spinner"></span>
              <span v-else>검색</span>
            </button>
          </div>
          <div v-if="recentSearches.length > 0" class="recent-tags">
            <span 
              v-for="(search, index) in recentSearches" 
              :key="index"
              class="recent-tag"
              @click="useRecentSearch(search)"
            >
              {{ search }}
            </span>
          </div>
        </div>
      </div>
      <div class="dashboard-body">
        <div class="widget-search-panel" v-show="hasSearched">
          <div class="search-results-container">
            <div v-if="isLoading" class="search-loading">
              <div class="ai-loading-text">AI가 열심히 찾고 있어요</div>
              <div class="ai-loading-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
            </div>
            <div v-else v-for="(result, idx) in searchResults" :key="idx" class="search-result-item" :class="{selected: isWidgetSelected(result), readonly: isWidgetSelected(result)}" @click="selectWidget(result)">
              <div class="result-name">{{ result.name }}</div>
            </div>
          </div>
        </div>
        <div class="widget-grid">
          <div v-for="n in 4" :key="n" class="widget-slot">
            <component
              v-if="selectedWidgets[n-1]"
              :is="selectedWidgets[n-1].componentName"
              v-bind="selectedWidgets[n-1].props"
              @close="removeWidget(n-1)"
            />
            <div v-else class="empty-slot">
              <lottie-player
                src="/assets/json/loading_ani.json"
                background="transparent"
                speed="1"
                style="width: 120px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"
                loop
                autoplay
              ></lottie-player>
            </div>
          </div>
        </div>
      </div>
      <div class="dashboard-footer">
        <div class="search-guide">
          <div class="guide-content">
            <div class="guide-item">
              <span class="guide-icon">🔍</span>
              <span class="guide-text">여러 위젯을 한 번에 검색하려면 쉼표(,)로 구분하세요</span>
            </div>
            <div class="guide-item">
              <span class="guide-icon">💡</span>
              <span class="guide-text">예시: "전력 사용량, 태양광 발전량, 배터리 상태"</span>
            </div>
          </div>
        </div>
        <button class="footer-close-btn" @click="$emit('close')" title="닫기">×</button>
      </div>
      <div v-if="toastMessage" class="toast-message">{{ toastMessage }}</div>
    </div>
  </div>
</template>

<script>
import api from '@/common/axios'
import EnergyGoalWidget from './energy/EnergyGoalWidget.vue'
import EnergyTrendWidget from './energy/EnergyTrendWidget.vue'
import EnergyUsageWidget from './energy/EnergyUsageWidget.vue'
import FacilityEnergyWidget from './energy/FacilityEnergyWidget.vue'
import PowerPeakWidget from './energy/PowerPeakWidget.vue'
import CarbonMonitorWidget from './energy/CarbonMonitorWidget.vue'
import EnergyAlertWidget from './energy/EnergyAlertWidget.vue'
import EnergyCostWidget from './energy/EnergyCostWidget.vue'
import EnergyTipWidget from './energy/EnergyTipWidget.vue'
import RenewableRatioWidget from './energy/RenewableRatioWidget.vue'

export default {
  name: 'DashboardWidgetGrid',
  components: {
    EnergyGoalWidget,
    EnergyTrendWidget,
    EnergyUsageWidget,
    FacilityEnergyWidget,
    PowerPeakWidget,
    CarbonMonitorWidget,
    EnergyAlertWidget,
    EnergyCostWidget,
    EnergyTipWidget,
    RenewableRatioWidget
  },
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedWidgets: [null, null, null, null],
      isLoading: false,
      toastMessage: '',
      hasSearched: false,
      recentSearches: [],
      widgetComponents: {}
    }
  },
  created() {
    this.loadRecentSearches()
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.searchInput) {
        this.$refs.searchInput.focus();
      }
    });
  },
  methods: {
    loadRecentSearches() {
      const searches = localStorage.getItem('recentSearches')
      if (searches) {
        this.recentSearches = JSON.parse(searches)
      }
    },
    saveRecentSearch(query) {
      let searches = this.recentSearches
      searches = searches.filter(s => s !== query)
      searches.unshift(query)
      searches = searches.slice(0, 5)
      this.recentSearches = searches
      localStorage.setItem('recentSearches', JSON.stringify(searches))
    },
    useRecentSearch(query) {
      this.searchQuery = query
      this.handleSearch()
    },
    async handleSearch() {
      if (!this.searchQuery.trim()) {
        this.showToast('검색어를 입력해주세요');
        return;
      }

      this.isLoading = true;
      this.hasSearched = true;
      try {
        const res = await api.post('/api/widgets/search', { query: this.searchQuery });
        this.searchResults = res.data.data;
        this.saveRecentSearch(this.searchQuery.trim())
      } catch (e) {
        this.searchResults = [];
        this.showToast('검색 중 오류가 발생했습니다');
      } finally {
        this.isLoading = false;
      }
    },
    showToast(msg) {
      this.toastMessage = msg;
      setTimeout(() => {
        this.toastMessage = '';
      }, 1800);
    },
    async loadWidgetComponent(componentName) {
      if (!componentName) {
        console.error('Component name is undefined')
        return null
      }

      if (!this.widgetComponents[componentName]) {
        try {
          const module = await import('/src/widgets/energy/' + componentName + '.vue')
          this.widgetComponents[componentName] = module.default
        } catch (error) {
          console.error(`Failed to load widget component: ${componentName}`, error)
          this.showToast('위젯 로드 중 오류가 발생했습니다')
          return null
        }
      }
      return this.widgetComponents[componentName]
    },
    async selectWidget(widget) {
      if (!widget || !widget.component_name) {
        console.error('Invalid widget data:', widget)
        return
      }

      if (this.isWidgetSelected(widget)) return
      const idx = this.selectedWidgets.findIndex(w => w === null)
      if (idx !== -1) {
        this.selectedWidgets[idx] = {
          ...widget,
          componentName: widget.component_name
        }
      }
    },
    isWidgetSelected(widget) {
      return this.selectedWidgets.some(w => w && w.id === widget.id)
    },
    removeWidget(idx) {
      this.selectedWidgets[idx] = null;
    }
  }
}
</script>

<style scoped>
.dashboard-dim {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  background: rgba(0,0,0,0.18);
  backdrop-filter: blur(2px);
}
.dashboard-widget-grid {
  position: relative;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  overflow: hidden;
  min-width: 900px;
  min-height: 600px;
}

.dashboard-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 24px 24px 16px;
  background: #fff;
  border-bottom: 1px solid #e9ecef;
}

.dashboard-body {
  flex: 1;
  display: flex;
  padding: 24px;
  gap: 24px;
  overflow: hidden;
  min-height: 480px;
  position: relative;
  z-index: 1;
  height: 100%;
}

.dashboard-footer {
  padding: 16px 24px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
  position: sticky;
  bottom: 0;
  z-index: 2;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-close-btn {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 20px;
  line-height: 30px;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: background 0.2s;
  margin-left: 16px;
}

.footer-close-btn:hover {
  background: #f5f5f5;
}

.widget-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 24px;
  min-height: 0;
  position: relative;
  z-index: 1;
  height: 100%;
}

.widget-slot {
  width: 565px;
  height: 246px;
  min-width: 565px;
  max-width: 565px;
  min-height: 246px;
  max-height: 246px;
  position: relative;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  overflow: hidden;
  display: flex;
  align-items: stretch;
  justify-content: stretch;
}

.widget-slot > * {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.search-container {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-area {
  display: flex;
  gap: 12px;
  width: 100%;
}

.search-input {
  flex: 1;
  height: 44px;
  padding: 0 16px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  font-size: 15px;
  color: #495057;
  background: #f8f9fa;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2355d6;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(35,85,214,0.1);
}

.search-btn {
  height: 44px;
  padding: 0 24px;
  border: none;
  border-radius: 8px;
  background: #2355d6;
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
}

.search-btn:hover:not(:disabled) {
  background: #1a44b0;
}

.search-btn:disabled {
  background: #e9ecef;
  color: #adb5bd;
  cursor: not-allowed;
}

.widget-search-panel {
  width: 140px;
  background: #e6f7ff;
  border-radius: 8px;
  padding: 12px 8px;
  margin-right: 18px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  box-shadow: 0 1px 4px rgba(35,85,214,0.07);
  transition: opacity 0.3s ease;
}

.search-results-container {
  overflow-y: auto;
  max-height: calc(100% - 20px);
  padding-right: 4px;
}

.search-result-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px 8px;
  margin-bottom: 4px;
  border-radius: 8px;
  background: #f8fafc;
  color: #222;
  font-size: 1em;
  cursor: pointer;
  transition: background 0.15s, box-shadow 0.15s;
}

.search-result-item:hover {
  background: #f0f4fa;
  border-radius: 8px;
}

.search-result-item.selected {
  border: 2px solid #2355d6;
  background: #e6f7ff;
  box-shadow: 0 2px 8px rgba(35,85,214,0.15);
}

.search-result-item.readonly {
  color: #bfc9d1;
  cursor: not-allowed;
  background: none;
  opacity: 0.7;
}

.search-result-item.selected.readonly {
  border: 2px solid #2355d6;
  background: #f5f5f5;
  color: #bfc9d1;
  cursor: not-allowed;
  opacity: 0.7;
}

.result-name {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-slot {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  z-index: 0;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.search-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #2355d6;
  font-weight: 500;
}

.ai-loading-text {
  margin-bottom: 12px;
  font-size: 1.1em;
}

.ai-loading-dots {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot {
  width: 8px;
  height: 8px;
  background: #2355d6;
  border-radius: 50%;
  display: inline-block;
  animation: blink 1.4s infinite both;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
  0%, 80%, 100% { opacity: 0.2; }
  40% { opacity: 1; }
}

.toast-message {
  position: fixed;
  left: 50%;
  bottom: 120px;
  transform: translateX(-50%);
  background: #222;
  color: #fff;
  padding: 10px 22px;
  border-radius: 22px;
  font-size: 1em;
  z-index: 9999;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
  opacity: 0.95;
  pointer-events: none;
  animation: toast-fadein 0.2s;
}

@keyframes toast-fadein {
  from { opacity: 0; transform: translateX(-50%) translateY(20px); }
  to { opacity: 0.95; transform: translateX(-50%) translateY(0); }
}

.ai-empty-text {
  margin-top: 12px;
  color: #2355d6;
  font-size: 1.1em;
  font-weight: 500;
  text-align: center;
  animation: ai-glow 2s infinite alternate;
}

@keyframes ai-glow {
  from { text-shadow: 0 0 8px #b3c6ff; }
  to { text-shadow: 0 0 18px #2355d6; }
}

.search-guide {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 24px;
}

.guide-content {
  display: flex;
  gap: 24px;
}

.guide-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.guide-icon {
  font-size: 16px;
}

.guide-text {
  font-size: 13px;
  color: #6c757d;
  line-height: 1.4;
}

.recent-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 0 4px;
}

.recent-tag {
  padding: 4px 12px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  font-size: 13px;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s ease;
}

.recent-tag:hover {
  background: #e9ecef;
  border-color: #dee2e6;
}
</style> 