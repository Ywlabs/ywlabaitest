<template>
  <div class="chat-container">
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
            <span v-html="renderMarkdown(msg.content)"></span>
          </template>
          <!-- route_type에 따라 버튼 분기 (routeList, getRouteInfo 의존성 제거) -->
          <button v-if="msg.type === 'ai' && msg.route_type === 'widget'"
                  @click="showWidget(msg.route_code, msg)"
                  class="action-button">
            {{ msg.route_name || '위젯 열기' }}
          </button>
          <button v-else-if="msg.type === 'ai' && msg.route_type === 'link'"
                  @click="navigateTo(msg.route_path)"
                  class="action-button">
            {{ msg.route_name || '자세히 보기' }}
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
             :disabled="isLoading"
             @keydown="handleInputKeydown"
        placeholder="질문을 입력하세요..."
             class="message-input">
      <button @click="sendMessage" class="send-button" :disabled="isLoading">전송</button>
    </div>
    <div class="ai-guide-banner">
      <span class="ai-icon">🤖</span>
      <span>영우랩스 AI가 동작중이에요. 궁금하신사항을 물어 보세요</span>
      <span class="ai-typing">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </span>
    </div>
    <div v-if="toastMessage" class="toast-message">{{ toastMessage }}</div>
  </div>
</template>

<script>
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'ChatInterface',
  emits: ['open-widget'],
  data() {
    return {
      messages: [],
      userInput: '',
      isLoading: false,
      toastMessage: ''
    }
  },
  mounted() {
    this.loadChatHistory();
    this.scrollToBottom();
  },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.chatMessages;
        if (el) {
          el.scrollTop = el.scrollHeight;
          el.scrollTop += 20;
        }
      });
    },
    renderMarkdown(text) {
      return DOMPurify.sanitize(marked(text || ''));
    },
    async loadChatHistory() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/chat/history`)
        const res = await response.json()
        if (res.status === 'success' && Array.isArray(res.data)) {
          const history = [...res.data].reverse();
          const formattedHistory = history.flatMap(item => {
            const arr = [];
            if (item.user_message && item.user_message.trim()) {
              arr.push({ type: 'user', content: item.user_message });
            }
            if (item.ai_response && item.ai_response.trim()) {
              arr.push({
                type: 'ai',
                content: item.ai_response,
                route_code: item.route_code,
                route_type: item.route_type,
                route_name: item.route_name,
                route_path: item.route_path,
                response_json: item.response_json
              });
            }
            return arr;
          });
          if (formattedHistory.length > 0) {
            this.messages = formattedHistory;
          } else {
            this.messages = [{
              type: 'ai',
              content: '안녕하세요! 영우랩스 AI 어시스턴트입니다. 무엇을 도와드릴까요?'
            }];
          }
          this.scrollToBottom();
        }
      } catch (error) {
        this.messages = [{
          type: 'ai',
          content: '안녕하세요! 영우랩스 AI 어시스턴트입니다. 무엇을 도와드릴까요?'
        }];
      }
    },
    async sendMessage() {
      if (this.isLoading) {
        this.showToast('현재 AI 가 활동중입니다. 잠시만 기다려 주세요');
        return;
      }
      if (!this.userInput.trim()) {
        this.showToast('질문 내용을 입력해 주세요');
        return;
      }
      this.messages.push({ type: 'user', content: this.userInput });
      const userMessage = this.userInput;
      this.userInput = '';
      this.isLoading = true;
      this.scrollToBottom();
      try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMessage })
        });
        const res = await response.json();
        const data = res.data;
        if (data) {
          this.messages.push({
            type: 'ai',
            content: data.response,
            route_code: data.route_code,
            route_type: data.route_type,
            route_name: data.route_name,
            route_path: data.route_path,
            response_json: { data }
          });
        }
      } catch (error) {
        let errorMessage = '요청하신 문의 사항에 대한 적절한 답변을 찾지 못하였습니다.';
        this.messages.push({ type: 'ai', content: errorMessage });
      } finally {
        this.isLoading = false;
        this.scrollToBottom();
      }
    },
    showWidget(route_code, msg = null) {
      let widgetProps = {}
      if (msg && msg.response_json && msg.response_json.data && msg.response_json.data.response_params) {
        widgetProps = { ...msg.response_json.data.response_params }
      }
      this.$emit('open-widget', { route_code, widgetProps })
    },
    navigateTo(path) {
      if (path) {
        this.$router.push(path)
      }
    },
    setUserInput(text) {
      this.userInput = text;
      this.$nextTick(() => {
        if (this.$refs.inputBox) this.$refs.inputBox.focus();
      });
    },
    handleInputKeydown(e) {
      if (this.isLoading) {
        this.showToast('현재 AI 가 활동중입니다. 잠시만 기다려 주세요');
        e.preventDefault();
        return;
      }
      if (e.key === 'Enter' && !this.userInput.trim()) {
        this.showToast('질문 내용을 입력해 주세요');
        e.preventDefault();
      }
    },
    showToast(msg) {
      this.toastMessage = msg;
      setTimeout(() => {
        this.toastMessage = '';
      }, 1800);
    }
  },
  watch: {
    isLoading(val) {
      if (val) this.scrollToBottom();
    }
  }
}
</script>

<style scoped>
.user-message {
  align-items: flex-end;
}
.user-message .message-content {
  background: #b3d8fd;
  color: #222;
  border-radius: 15px 15px 15px 15px;
  margin-left: 30%;
  max-width: 70%;
  padding: 2px 14px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  font-size: 0.98em;
}

.ai-message {
  align-items: flex-start;
}
.ai-message .message-content {
  background: #f8f9fa;
  color: #333;
  border-radius: 15px 15px 15px 15px;
  margin-right: 0;
  max-width: 100%;
  padding: 4px 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  font-size: 0.98em;
}

/* 마크다운 표 스타일 (구분선 포함) */
.ai-message .message-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  max-width: 90%;
  margin: 10px 0 10px 0;
  margin-left: 0;
  margin-right: auto;
  border: 1px solid #bfc9d1;
}
.ai-message .message-content :deep(th),
.ai-message .message-content :deep(td) {
  border: 1px solid #bfc9d1;
  padding: 8px;
  text-align: left;
}
.ai-message .message-content :deep(th) {
  background: #e6eaf1;
  font-weight: 600;
  color: #2355d6;
}
.ai-message .message-content :deep(tr:nth-child(even)) {
  background: #f9f9f9;
}

.ai-message .message-content :deep(ul),
.ai-message .message-content :deep(ol) {
  margin-left: 0;
  margin-right: auto;
  padding-left: 10px;
  max-width: 90%;
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
  margin-top: 6px;
  padding: 4px 12px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
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
  .chat-container {
    height: 50vh;
  }
}

.user-message + .ai-message {
  margin-top: 32px;
}
.ai-message + .user-message {
  margin-top: 40px;
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
</style> 