<template>
  <div class="home">
    <div class="layout-container">
      <!-- Left Column (30%) -->
      <div class="left-column">
        <div class="widget-container">
          <div class="widget top-widget">
            <TodayVacation />
          </div>
          <div class="widget bottom-widget">
            <component v-if="activeWidgetComponent" :is="activeWidgetComponent" :key="activeWidgetKey" />
            <div v-else class="empty-widget-message">
              위젯을 선택하면 이 영역에 표시됩니다.
            </div>
          </div>
        </div>
      </div>

      <!-- Center Column (40%) -->
      <div class="center-column">
        <div class="chat-container" ref="chatContainer">
          <div class="chat-messages" ref="chatMessages">
            <div class="ai-guide-banner">
              <span class="ai-icon">🤖</span>
              <span>영우랩스 AI가 동작중입니다. 궁금하신사항을 물어 보세요</span>
              <span class="ai-typing">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>
            </div>
            <div v-for="(message, index) in messages" :key="index" 
                 :class="['message', message.type === 'user' ? 'user-message' : 'ai-message']">
              <div class="message-content">
                <template v-if="message.employee">
                  <table class="employee-info-table">
                    <tbody>
                      <tr><th>이름</th><td>{{ message.employee.name }}</td></tr>
                      <tr><th>직책</th><td>{{ message.employee.position }}</td></tr>
                      <tr><th>부서</th><td>{{ message.employee.dept_nm }}</td></tr>
                      <tr><th>이메일</th><td>{{ message.employee.email }}</td></tr>
                      <tr><th>연락처</th><td>{{ message.employee.phone }}</td></tr>
                    </tbody>
                  </table>
                </template>
                <template v-else>
                  <div v-html="formatMessage(message.content)"></div>
                </template>
                <!-- widget 유형이면 버튼 표시 -->
                <button v-if="message.type === 'ai' && message.route_type === 'widget' && message.route_code"
                        @click="showWidget(message.route_code)"
                        class="action-button">
                  {{ message.route_name || '위젯 열기' }}
                </button>
                <!-- link 유형이면 버튼 표시 -->
                <button v-else-if="message.type === 'ai' && message.route_type === 'link' && message.route_path"
                        @click="navigateTo(message.route_path)"
                        class="action-button">
                  {{ message.route_name || '자세히 보기' }}
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
import FloatingMenu from '@/components/FloatingMenu.vue'
import TodayVacation from '@/components/TodayVacation.vue'
import OrganizationChart from '@/components/OrganizationChart.vue'
import axios from 'axios'
import { markRaw } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

// axios 인스턴스 생성
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30초 타임아웃
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true // CORS 요청에 credentials 포함
});

const widgetMap = {
  ORG_CHART: () => import('@/widgets/OrganizationWidget.vue'),
  // 앞으로 추가될 위젯은 Widget 네이밍 사용
}

export default {
  name: 'Home',
  components: { 
    FloatingMenu,
    TodayVacation,
    OrganizationChart
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
    }
  },
  async created() {
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
    async loadChatHistory() {
      try {
        const response = await api.get('/api/chat/history')
        if (response.data && response.data.status === 'success' && Array.isArray(response.data.data)) {
          // 최신순으로 정렬
          const history = [...response.data.data].reverse();
          // 각 item마다 [질문, 답변] 순서로 메시지 추가
          const formattedHistory = history.map(item => [
            { type: 'user', content: item.user_message },
            { 
              type: 'ai', 
              content: item.ai_response || '죄송합니다. 응답을 생성하지 못했습니다.',
              route_code: item.route_code,
              route_type: item.route_type,
              route_name: item.route_name,
              route_path: item.route_path
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
            employee: data.employee,
            response_type: data.response_type,
            route_code: data.route_code,
            route_type: data.route_type,
            route_name: data.route_name,
            route_path: data.route_path
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
    async showWidget(route_code) {
      if (widgetMap[route_code]) {
        const comp = (await widgetMap[route_code]()).default
        this.activeWidgetComponent = markRaw(comp)
        this.activeWidgetCode = route_code
        this.activeWidgetKey += 1
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
.home {
  width: 100%;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
  font-size: 0.9em;
}

.layout-container {
  display: flex;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 40px);
  align-items: flex-start;
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
  flex: 4;
  display: flex;
  flex-direction: column;
  height: 80%;
  box-sizing: border-box;
}

.right-column {
  flex: 3;
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 80%;
  box-sizing: border-box;
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

.message {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.user-message {
  align-items: flex-end;
}

.user-message .message-content {
  background: #007bff;
  color: white;
}

.ai-message {
  align-items: flex-start;
}

.ai-message .message-content {
  background: #f8f9fa;
  color: #333;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 15px;
  background: #f0f0f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
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
}

.action-button:hover {
  background: #218838;
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
  color: #aaa;
  text-align: center;
  padding: 40px 0;
  font-size: 1.1em;
}

.ai-guide-banner {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e6f7ff;
  color: #007bff;
  font-weight: 500;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 10px 0;
  font-size: 0.95em;
  position: sticky;
  top: 0;
  z-index: 2;
}
.ai-icon {
  margin-right: 8px;
  font-size: 1.3em;
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
</style> 