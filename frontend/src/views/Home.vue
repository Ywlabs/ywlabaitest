<template>
  <div class="home">
    <AnimationBackground />
    <div class="layout-container">
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
                @close="activeWidgetComponent = null"
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
        <div class="chat-container" ref="chatContainer">
          <div class="chat-messages" ref="chatMessages">
            <div v-for="(msg, idx) in messages" :key="idx" :class="[msg.type === 'user' ? 'user-message' : 'ai-message']">
              <div class="message-content">
                <!-- AI 메시지이면서 직원 정보가 구조화되어 있으면 표로 출력 -->
                <template v-if="msg.type === 'ai' && msg.response_json && msg.response_json.data && msg.response_json.data.employee">
                  <table class="employee-table">
                    <tbody>
                      <tr><th>이름</th><td>{{ msg.response_json.data.employee.name }}</td></tr>
                      <tr><th>직책</th><td>{{ msg.response_json.data.employee.position }}</td></tr>
                      <tr><th>부서</th><td>{{ msg.response_json.data.employee.dept_nm }}</td></tr>
                      <tr><th>이메일</th><td>{{ msg.response_json.data.employee.email }}</td></tr>
                      <tr><th>연락처</th><td>{{ msg.response_json.data.employee.phone }}</td></tr>
                    </tbody>
                  </table>
                </template>
                <!-- 그 외에는 기존 텍스트 출력 -->
                <template v-else>
                  <span v-html="formatMessage(msg.content)"></span>
                </template>
                <!-- route_code가 있으면 getRouteInfo로 route_type 분기 -->
                <button v-if="msg.type === 'ai' && msg.route_code && getRouteInfo(msg.route_code)?.route_type === 'widget'"
                        @click="showWidget(msg.route_code, msg)"
                        class="action-button">
                  {{ getRouteInfo(msg.route_code)?.route_name || '위젯 열기' }}
                </button>
                <button v-else-if="msg.type === 'ai' && msg.route_code && getRouteInfo(msg.route_code)?.route_type === 'link'"
                        @click="navigateTo(getRouteInfo(msg.route_code)?.route_path)"
                        class="action-button">
                  {{ getRouteInfo(msg.route_code)?.route_name || '자세히 보기' }}
                </button>
              </div>
            </div>
            <!-- 로딩 애니메이션 -->
            <div v-if="isLoading" class="loading-indicator">
              <span class="spinner"></span> 조회중입니다...
            </div>
          </div>
          <div class="chat-input">
            <input type="text" 
                   v-model="userInput" 
                   ref="inputBox"
                   @keyup.enter="sendMessage"
                   placeholder="질문을 입력하세요..."
                   class="message-input">
            <button @click="sendMessage" class="send-button">전송</button>
          </div>
          <div class="ai-guide-banner">
            <span class="ai-icon">🤖</span>
            <span>영우랩스 AI가 동작중입니다. 궁금하신사항을 물어 보세요</span>
            <span class="ai-typing">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </span>
          </div>
        </div>
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
    <FloatingMenu />
  </div>
</template>

<script>
import AnimationBackground from '@/components/AnimationBackground.vue'
import FloatingMenu from '@/components/FloatingMenu.vue'
import EnvironmentWidget from '@/widgets/EnvironmentWidget.vue'
import OrganizationChart from '@/components/OrganizationChart.vue'
import SalesWidget from '@/widgets/SalesWidget.vue'
import axios from 'axios'
import { markRaw } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

const widgetMap = {
  ORG_CHART: () => import('@/widgets/OrganizationWidget.vue'),
  SALES_WIDGET: () => import('@/widgets/SalesWidget.vue'),
  // 앞으로 추가될 위젯은 Widget 네이밍 사용
}

// axios 인스턴스 생성
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // CORS 요청에 credentials 포함
});

export default {
  name: 'Home',
  components: { 
    AnimationBackground,
    FloatingMenu,
    EnvironmentWidget,
    OrganizationChart,
    SalesWidget
  },
  data() {
    return {
      userInput: '',
      messages: [
        {
          type: 'ai',
          content: '안녕하세요! 영우랩스 AI 어시스턴트입니다. 무엇을 도와드릴까요?'
        }
      ],
      isLoading: false,
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
      activeWidgetProps: {}
    }
  },
  async created() {
    await this.loadRoutes() // 앱 로딩 시 routes 정보 먼저 가져옴
    await this.loadChatHistory()
    this.fetchPopularQuestions()
  },
  mounted() {
    this.scrollToBottom();
    this.startTyping();
    this.cursorInterval = setInterval(() => {
      this.showCursor = !this.showCursor;
    }, 500);
  },
  beforeDestroy() {
    clearInterval(this.typingInterval);
    clearInterval(this.cursorInterval);
  },
  methods: {
    // routes 정보를 API로 받아와 저장
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
    // route_code로 route 정보 조회
    getRouteInfo(route_code) {
      return this.routeList.find(r => r.route_code === route_code)
    },
    async loadChatHistory() {
      try {
        const response = await api.get('/api/chat/history')
        if (response.data && response.data.status === 'success' && Array.isArray(response.data.data)) {
          // 최신순으로 정렬
          const history = [...response.data.data].reverse();
          // 각 item마다 [질문, 답변] 순서로 메시지 추가 (response_json 포함)
          const formattedHistory = history.map(item => [
            { type: 'user', content: item.user_message },
            { 
              type: 'ai', 
              content: item.ai_response || '죄송합니다. 응답을 생성하지 못했습니다.',
              route_code: item.route_code,
              route_type: item.route_type,
              route_name: item.route_name,
              route_path: item.route_path,
              response_json: item.response_json // 구조화 응답 포함
            }
          ]).flat();
          this.messages = formattedHistory;
          this.scrollToBottom();
        } else {
          console.error('Invalid history data format:', response.data)
          this.messages = []
        }
      } catch (error) {
        console.error('채팅 히스토리 로딩 중 오류 발생:', error)
        this.messages = []
      }
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
      this.userInput = q
      this.$refs.inputBox && this.$refs.inputBox.focus()
    },
    async sendMessage() {
      if (!this.userInput.trim()) return
      this.messages.push({ type: 'user', content: this.userInput })
      const userMessage = this.userInput
      this.userInput = ''
      this.isLoading = true
      try {
        const response = await api.post('/api/chat', { 
          message: userMessage
        })
        const data = response.data.data
        if (data) {
          this.messages.push({
            type: 'ai',
            content: data.response,
            route_code: data.route_code,
            route_type: data.route_type,
            route_name: data.route_name,
            route_path: data.route_path,
            response_json: { data } // 구조화 응답 포함
          })
        }
        this.fetchPopularQuestions()
      } catch (error) {
        console.error('Error:', error)
        let errorMessage = '죄송합니다. 오류가 발생했습니다.'
        if (error.code === 'ECONNABORTED') {
          errorMessage = '요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.'
        } else if (error.response) {
          errorMessage = error.response.data.message || errorMessage
        }
        this.messages.push({ type: 'ai', content: errorMessage })
      } finally {
        this.isLoading = false
        this.scrollToBottom()
      }
    },
    formatMessage(content) {
      if (!content) return ''
      
      return String(content)
        .replace(/\[.*?\]\(.*?\)/g, '') // 마크다운 링크 제거
        .replace(/\s+/g, ' ') // 불필요한 공백 정리
        .replace(/\n/g, '<br>')
    },
    async showWidget(route_code, msg = null) {
      if (widgetMap[route_code]) {
        const comp = (await widgetMap[route_code]()).default
        // response_params를 위젯에 prop으로 그대로 전달 (범용)
        let widgetProps = {}
        if (msg && msg.response_json && msg.response_json.data && msg.response_json.data.response_params) {
          widgetProps = { ...msg.response_json.data.response_params }
        }
        this.activeWidgetComponent = markRaw(comp)
        this.activeWidgetCode = route_code
        this.activeWidgetKey += 1
        this.activeWidgetProps = widgetProps
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
          // 스크롤이 짤리지 않도록 추가 여백 확보
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
    }
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
/* ===== 기존 스타일 백업 (아래 새 스타일 적용, 이상하면 이 부분 복원) =====
기존 스타일 전체는 이 주석 안에 있습니다. 필요시 복원하세요.
*/

.message {
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
}

/* 질문(오른쪽, 파란 말풍선) */
.user-message {
  align-items: flex-end;
}
.user-message .message-content {
  background: linear-gradient(135deg, #4f8cff 0%, #2355d6 100%);
  color: #fff;
  border-radius: 18px !important;
  margin-left: 25%;
  max-width: 70%;
  padding: 16px 22px;
  font-size: 1.05em;
  box-shadow: 0 4px 16px rgba(79,140,255,0.08);
  position: relative;
  word-break: break-word;
  transition: background 0.2s;
}

/* 답변(왼쪽, 흰색 말풍선+그림자) */
.ai-message {
  align-items: flex-start;
}
.ai-message .message-content {
  background: #fff;
  color: #222;
  border-radius: 18px !important;
  margin-right: 25%;
  max-width: 70%;
  padding: 16px 22px;
  font-size: 1.05em;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  position: relative;
  word-break: break-word;
  border: 1px solid #e6eaf1;
  transition: background 0.2s;
}

/* 말풍선 꼬리(선택, 더 세련되게 하고 싶을 때) */
.user-message .message-content::after {
  content: '';
  position: absolute;
  right: -12px;
  bottom: 12px;
  border-width: 8px 0 8px 12px;
  border-style: solid;
  border-color: transparent transparent transparent #4f8cff;
  filter: drop-shadow(0 2px 2px rgba(79,140,255,0.08));
}
.ai-message .message-content::after {
  content: '';
  position: absolute;
  left: -12px;
  bottom: 12px;
  border-width: 8px 12px 8px 0;
  border-style: solid;
  border-color: transparent #fff transparent transparent;
  filter: drop-shadow(0 2px 2px rgba(0,0,0,0.08));
}

/* 표(직원 정보)는 카드 느낌 */
.employee-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 12px 0 8px 0;
  background: #f7faff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.07);
  overflow: hidden;
}
.employee-table th {
  background: #e6eaf1;
  text-align: left;
  padding: 8px 14px;
  font-weight: 600;
  color: #2355d6;
  width: 90px;
  border-bottom: 1px solid #e6eaf1;
}
.employee-table td {
  background: #f7faff;
  padding: 8px 14px;
  color: #222;
  border-bottom: 1px solid #e6eaf1;
}
.employee-table tr:last-child th,
.employee-table tr:last-child td {
  border-bottom: none;
}

/* 버튼(더 둥글고 컬러풀하게) */
.action-button {
  margin-top: 18px;
  padding: 10px 24px;
  background: linear-gradient(90deg, #4f8cff 0%, #2355d6 100%);
  color: #fff;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(79,140,255,0.10);
  transition: background 0.2s, box-shadow 0.2s;
  display: block;
  width: auto;
}
.action-button:hover {
  background: linear-gradient(90deg, #2355d6 0%, #4f8cff 100%);
  box-shadow: 0 4px 16px rgba(79,140,255,0.15);
}
.action-button + .action-button {
  margin-top: 10px;
}

/* 질문-답변 쌍 사이 간격 */
.user-message + .ai-message,
.ai-message + .user-message {
  margin-top: 40px;
}

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
  margin: 32px auto 0 auto;
  height: calc(100vh - 40px);
  align-items: flex-start;
  position: relative;
}

.left-column, .center-column, .right-column {
  font-size: 0.92em;
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
  margin-right: 30%;
  max-width: 70%;
  padding: 12px 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  font-size: 0.98em;
}

.employee-table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0 8px 0;
}
.employee-table th {
  background: #f0f0f0;
  text-align: left;
  padding: 4px 8px;
  font-weight: bold;
  width: 80px;
}
.employee-table td {
  background: #fff;
  padding: 4px 8px;
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