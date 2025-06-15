<template>
  <div class="home">
    <AnimationBackground />
    <div class="layout-container" ref="layoutContainer">
      <!-- Left Column (30%) -->
      <div class="left-column">
        <div class="widget-container">
          <div class="widget top-widget">
            <EnvironmentWidget />
          </div>
          <div class="widget bottom-widget">
            <transition name="fade-widget" mode="out-in">
              <component
                v-if="activeWidgetComponent"
                :is="activeWidgetComponent"
                v-bind="activeWidgetProps"
                :key="activeWidgetKey"
                @close="closeWidget"
              />
              <div v-else class="empty-widget-message">
                <lottie-player
                  src="/assets/json/ai-animation.json"
                  background="transparent"
                  speed="1"
                  style="width: 120px; height: 120px;"
                  loop
                  autoplay
                ></lottie-player>
                <div class="ai-empty-text">
                  <span>AI 위젯 준비중입니다.</span>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Center Column (40%) -->
      <div class="center-column">
        <ChatInterface ref="chatRef" @open-widget="handleOpenWidget" />
      </div>

      <!-- Right Column (30%) -->
      <div class="right-column">
        <div class="popular-questions">
          <h4>많이 검색된 질문</h4>
          <ul>
            <li v-for="(q, idx) in popularQuestions" :key="idx" @click="setPrompt(q)">
              {{ q }}
            </li>
          </ul>
        </div>
      </div>
    </div>
    <!-- 오버레이: DASHBOARD_WIDGET일 때만 표시 -->
    <div v-if="showDashboardOverlay">
      <!-- 반투명 블러 배경 -->
      <div 
        class="dashboard-overlay-backdrop" 
        @wheel.prevent 
        @touchmove.prevent 
        @mousedown.prevent 
        @click.prevent
        style="position: fixed; left: 0; top: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.25); backdrop-filter: blur(2px); z-index: 999;"
      ></div>
      <!-- 오버레이 위젯 -->
      <div :style="{ ...dashboardOverlayStyle, cursor: 'move' }" class="dashboard-overlay" @mousedown="onOverlayHeaderMouseDown">
        <component
          v-if="dashboardWidgetComponent"
          :is="dashboardWidgetComponent"
          @close="showDashboardOverlay = false"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AnimationBackground from '@/components/AnimationBackground.vue'
import EnvironmentWidget from '@/widgets/EnvironmentWidget.vue'
import SalesWidget from '@/widgets/SalesWidget.vue'
import ChatInterface from '@/components/ChatInterface.vue'
import api from '@/common/axios'
import { markRaw, defineAsyncComponent } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const ENERGY_WIDGET = defineAsyncComponent(() => import('@/widgets/DashboardWidgetGrid.vue'))

const widgetMap = {
  ORG_CHART: () => import('@/widgets/OrganizationWidget.vue'),
  SALES_WIDGET: () => import('@/widgets/SalesWidget.vue'),
  DASHBOARD_WIDGET: () => ENERGY_WIDGET,
  // 앞으로 추가될 위젯은 Widget 네이밍 사용
}

export default {
  name: 'Home',
  components: { 
    AnimationBackground,
    EnvironmentWidget,
    SalesWidget,
    ChatInterface
  },
  data() {
    return {
      fullText: '영우랩스 AI가 동작중입니다.',
      animatedText: '',
      showCursor: true,
      typingIndex: 0,
      typingInterval: null,
      cursorInterval: null,
      popularQuestions: [],
      activeWidgetCode: null,
      activeWidgetComponent: null,
      activeWidgetKey: 0,
      routeList: [], // routes 정보를 저장
      activeWidgetProps: {},
      dashboardOverlayStyle: {},
      showDashboardOverlay: false,
      dashboardWidgetComponent: null,
      dragOffset: { x: 0, y: 0 },
      isDragging: false,
      dragStart: { x: 0, y: 0 },
      overlayPos: null, // 드래그 시 top/left
    }
  },
  async created() {
    await this.loadRoutes() // 앱 로딩 시 routes 정보 먼저 가져옴
    this.fetchPopularQuestions()
  },
  mounted() {
    this.scrollToBottom();
    this.startTyping();
    this.cursorInterval = setInterval(() => {
      this.showCursor = !this.showCursor;
    }, 500);
    this.loadLastWidget();
  },
  beforeDestroy() {
    clearInterval(this.typingInterval);
    clearInterval(this.cursorInterval);
  },
  methods: {
    async loadRoutes() {
      try {
        const res = await api.get('/api/routes')
        if (res.data && res.data.status === 'success') {
          this.routeList = res.data.data
        }
      } catch (e) {
        this.routeList = []
      }
    },
    getRouteInfo(route_code) {
      return this.routeList.find(r => r.route_code === route_code)
    },
    async fetchPopularQuestions() {
      try {
        const { data } = await api.get('/api/chat/popular')
        this.popularQuestions = data
      } catch (e) {
        this.popularQuestions = []
      }
    },
    setPrompt(q) {
      if (this.$refs.chatRef && this.$refs.chatRef.setUserInput) {
        this.$refs.chatRef.setUserInput(q);
      }
    },
    async handleOpenWidget({ route_code, widgetProps }) {
      const code = route_code ? route_code.toUpperCase() : '';
      console.log('route_code:', route_code, 'code:', code); // 디버깅용
      if (code === 'DASHBOARD_WIDGET') {
        const comp = (await widgetMap[code]()).default;
        this.dashboardWidgetComponent = markRaw(comp);
        this.$nextTick(() => {
          const layout = this.$refs.layoutContainer;
          if (layout) {
            const rect = layout.getBoundingClientRect();
            const minHeight = 600;
            const maxHeight = Math.max(window.innerHeight * 0.9, minHeight);
            // 중앙 정렬로 시작
            this.overlayPos = null;
            this.dashboardOverlayStyle = {
              position: 'fixed',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: rect.width + 'px',
              minHeight: minHeight + 'px',
              maxHeight: maxHeight + 'px',
              zIndex: 1000,
              overflow: 'hidden',
              transition: 'opacity 0.3s'
            };
            this.showDashboardOverlay = true;
          }
        });
      } else if (widgetMap[code]) {
        const comp = (await widgetMap[code]()).default
        this.activeWidgetComponent = markRaw(comp)
        this.activeWidgetKey += 1
        this.activeWidgetProps = widgetProps
        localStorage.setItem('lastAiWidget', JSON.stringify({ route_code, widgetProps }));
      }
    },
    closeWidget() {
      this.activeWidgetComponent = null;
      localStorage.removeItem('lastAiWidget');
    },
    async loadLastWidget() {
      const last = localStorage.getItem('lastAiWidget');
      if (last) {
        try {
          const { route_code, widgetProps } = JSON.parse(last);
          await this.handleOpenWidget({ route_code, widgetProps });
        } catch (e) {
          // 파싱 에러 등 예외 무시
        }
      }
    },
    navigateTo(path) {
      if (path) {
        this.$router.push(path)
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.chatMessages;
        if (el) {
          el.scrollTop = el.scrollHeight;
          el.scrollTop += 20;
        }
      });
    },
    startTyping() {
      this.animatedText = '';
      this.typingIndex = 0;
      this.typingInterval = setInterval(() => {
        if (this.typingIndex < this.fullText.length) {
          this.animatedText += this.fullText[this.typingIndex];
          this.typingIndex++;
        } else {
          clearInterval(this.typingInterval);
        }
      }, 50);
    },
    onOverlayHeaderMouseDown(e) {
      // 드래그 시작: transform 제거, top/left로 전환
      const popup = e.target.closest('.dashboard-overlay');
      if (!popup) return;
      const rect = popup.getBoundingClientRect();
      this.isDragging = true;
      this.dragStart = { x: e.clientX, y: e.clientY };
      this.dragOffset = { x: rect.left, y: rect.top };
      this.overlayPos = { top: rect.top, left: rect.left };
      // transform 제거, top/left로 전환
      this.dashboardOverlayStyle = {
        ...this.dashboardOverlayStyle,
        top: rect.top + 'px',
        left: rect.left + 'px',
        transform: '',
      };
      document.addEventListener('mousemove', this.onOverlayMouseMove);
      document.addEventListener('mouseup', this.onOverlayMouseUp);
    },
    onOverlayMouseMove(e) {
      if (!this.isDragging) return;
      const dx = e.clientX - this.dragStart.x;
      const dy = e.clientY - this.dragStart.y;
      const newLeft = this.dragOffset.x + dx;
      const newTop = this.dragOffset.y + dy;
      this.overlayPos = { top: newTop, left: newLeft };
      this.dashboardOverlayStyle = {
        ...this.dashboardOverlayStyle,
        top: newTop + 'px',
        left: newLeft + 'px',
        transform: '',
      };
    },
    onOverlayMouseUp() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.onOverlayMouseMove);
      document.removeEventListener('mouseup', this.onOverlayMouseUp);
    },
  },
  watch: {
    messages() {
      this.scrollToBottom();
    },
    isLoading() {
      this.scrollToBottom();
    }
  }
}
</script>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  font-size: 0.9em;
  position: relative; /* 배경 위에 오도록 */
  z-index: 1;
  overflow: hidden; /* 배경이 영역을 벗어나지 않게 */
}

.layout-container {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 100px auto 0 auto;
  height: calc(100vh - 40px);
  align-items: flex-start;
  position: relative;
}

.left-column {
  flex: 3;
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 80%;
  box-sizing: border-box;
}

.widget-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 20px;
}

.widget {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex: 1;
  min-height: 0; /* 중요: flex-grow가 제대로 작동하도록 */
  overflow: auto;
}

.top-widget {
  flex: 1;
}

.bottom-widget {
  flex: 1;
}

.center-column {
  flex: 3.5;
  display: flex;
  flex-direction: column;
  height: 80%;
  box-sizing: border-box;
}

.right-column {
  flex: 1.3;
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 80%;
  box-sizing: border-box;
}

.user-message {
  align-items: flex-end;
}
.user-message .message-content {
  background: #007bff;
  color: white;
  border-radius: 15px 15px 2px 15px;
  margin-left: 30%;
  max-width: 70%;
  padding: 12px 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  font-size: 0.98em;
}

.ai-message {
  align-items: flex-start;
}
.ai-message .message-content {
  background: #f8f9fa;
  color: #333;
  border-radius: 15px 15px 15px 2px;
  margin-right: 0;
  max-width: 100%;
  padding: 12px 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  font-size: 0.98em;
}

/* 마크다운 표 스타일 (구분선 포함) */
.ai-message .message-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 10px 0;
}
.ai-message .message-content th,
.ai-message .message-content td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.ai-message .message-content th {
  background: #e6eaf1;
  font-weight: 600;
  color: #2355d6;
}
.ai-message .message-content tr:nth-child(even) {
  background: #f9f9f9;
}

/* 마크다운 리스트, 코드 등 스타일 */
.ai-message .message-content ul,
.ai-message .message-content ol {
  margin: 10px 0 10px 24px;
}
.ai-message .message-content code {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-size: 0.95em;
}
.ai-message .message-content pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  font-size: 0.98em;
}

.company-info {
  text-align: center;
  padding: 20px;
}

.company-info h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.company-info p {
  color: #666;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  font-size: 0.92em;
}

.chat-input {
  display: flex;
  padding: 20px;
  background: #fff;
  border-top: 1px solid #eee;
  gap: 10px;
  font-size: 0.92em;
}

.message-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 13px;
  max-height: 60px;
  min-height: 36px;
  resize: vertical;
}

.send-button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
  font-size: 13px;
}

.send-button:hover {
  background: #0056b3;
}

.action-button {
  margin-top: 10px;
  padding: 8px 16px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
  display: block;
  width: auto;
}

.action-button:hover {
  background: #218838;
}

.ai-message .action-button {
  margin-top: 16px;
}

.action-button + .action-button {
  margin-top: 8px;
}

.popular-questions {
  height: 100%;
  overflow-y: auto;
}

.popular-questions h4 {
  margin-bottom: 1rem;
  color: #007bff;
  font-size: 1.1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #007bff;
}

.popular-questions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.popular-questions li {
  padding: 0.8rem 1rem;
  margin-bottom: 0.5rem;
  background: white;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.popular-questions li:hover {
  background: #e6f7ff;
  transform: translateX(5px);
}

.ai-guide {
  text-align: center;
  color: #007bff;
  font-weight: 500;
  margin-bottom: 8px;
  margin-top: 8px;
  font-size: 1.1rem;
  letter-spacing: 0.02em;
  min-height: 1.5em;
}

.typing-cursor {
  display: inline-block;
  width: 1ch;
  animation: blink 1s steps(1) infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #007bff;
  font-weight: 500;
  margin: 10px 0;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid #42b983;
  border-top: 3px solid #e0e0e0;
  border-radius: 50%;
  margin-right: 10px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-widget-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #2355d6;
  font-size: 1.15em;
  padding: 40px 0;
  min-height: 180px;
  background: #f7faff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.07);
}
.ai-empty-text span {
  font-weight: 600;
  letter-spacing: 0.02em;
  margin-top: 12px;
  animation: ai-glow 2s infinite alternate;
}
@keyframes ai-glow {
  from { text-shadow: 0 0 8px #b3c6ff; }
  to { text-shadow: 0 0 18px #2355d6; }
}

.ai-guide-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e6f7ff;
  color: #007bff;
  font-weight: 500;
  border-radius: 8px;
  margin: 4px 32px 8px 32px;
  padding: 10px 0;
  font-size: 0.97em;
  width: auto;
  min-height: 38px;
  box-sizing: border-box;
}
.ai-icon {
  margin-right: 8px;
  font-size: 1.5em;
  line-height: 1;
}
.ai-typing {
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.dot {
  width: 7px;
  height: 7px;
  margin: 0 1.5px;
  background: #007bff;
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

@media (max-width: 1200px) {
  .layout-container {
    flex-direction: column;
    height: auto;
  }

  .left-column,
  .center-column,
  .right-column {
    width: 100%;
    margin-bottom: 20px;
    height: auto;
  }

  .chat-container {
    height: 50vh;
  }
}

/* 질문과 답변(즉, user-message와 ai-message) 사이의 간격을 넓게 */
.user-message + .ai-message {
  margin-top: 32px;
}
/* 답변 다음에 새로운 질문이 시작될 때도 간격을 넓게 */
.ai-message + .user-message {
  margin-top: 40px;
}

/* ===== Fade-in, Fade-out 애니메이션 효과 (위젯용) ===== */
.fade-widget-enter-active, .fade-widget-leave-active {
  transition: opacity 0.35s cubic-bezier(0.4,0,0.2,1);
}
.fade-widget-enter-from, .fade-widget-leave-to {
  opacity: 0;
}
.fade-widget-enter-to, .fade-widget-leave-from {
  opacity: 1;
}
</style> 