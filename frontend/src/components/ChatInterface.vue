<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" 
           :class="['message', message.type]">
        <div class="message-content">
          {{ message.content }}
          <div v-if="message.type === 'button_action' && message.button_text" class="action-buttons">
            <button @click="handleButtonAction(message.target_url)" class="action-button">
              {{ message.button_text }}
            </button>
          </div>
        </div>
        
      </div>
    </div>
    <div class="chat-input">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage"
        placeholder="질문을 입력하세요..."
        type="text"
      >
      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import SalesWidget from '../widgets/SalesWidget.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

export default {
  name: 'ChatInterface',
  components: { SalesWidget },
  setup() {
    const messages = ref([])
    const userInput = ref('')
    const messagesContainer = ref(null)
    const router = useRouter()
    const openedSalesWidgets = ref([])

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    const handleButtonAction = (targetUrl) => {
      if (targetUrl) {
        router.push(targetUrl)
      }
    }

    const openSalesWidget = (idx) => {
      if (!openedSalesWidgets.value.includes(idx)) {
        openedSalesWidgets.value.push(idx)
      }
    }

    const closeSalesWidget = (idx) => {
      openedSalesWidgets.value = openedSalesWidgets.value.filter(i => i !== idx)
    }

    const sendMessage = async () => {
      if (!userInput.value.trim()) return

      messages.value.push({
        type: 'user',
        content: userInput.value
      })

      const userMessage = userInput.value
      userInput.value = ''

      try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userMessage })
        })

        const data = await response.json()

        messages.value.push({
          type: data.type === 'page_redirect' ? 'system' : 'ai',
          content: data.content,
          target_url: data.target_url,
          button_text: data.button_text,
          route_code: data.route_code
        })

        if (data.type === 'page_redirect' && data.target_url) {
          setTimeout(() => {
            router.push(data.target_url)
          }, 1500)
        }

        await scrollToBottom()
      } catch (error) {
        console.error('Error:', error)
        messages.value.push({
          type: 'error',
          content: '죄송합니다. 오류가 발생했습니다. 다시 시도해 주세요.'
        })
      }
    }

    onMounted(() => {
      messages.value.push({
        type: 'ai',
        content: '안녕하세요! 영우랩스 AI 어시스턴트입니다. 무엇을 도와드릴까요?'
      })
    })

    return {
      messages,
      userInput,
      messagesContainer,
      sendMessage,
      handleButtonAction,
      openedSalesWidgets,
      openSalesWidget,
      closeSalesWidget
    }
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  height: 80vh;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 10px;
  margin-bottom: 20px;
}

.message {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 15px;
  word-wrap: break-word;
}

.user {
  align-items: flex-end;
}

.user .message-content {
  background: #007bff;
  color: white;
}

.ai .message-content {
  background: white;
  border: 1px solid #ddd;
}

.system .message-content {
  background: #e9ecef;
  color: #495057;
}

.error .message-content {
  background: #dc3545;
  color: white;
}

.chat-input {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background: #0056b3;
}

.action-buttons {
  margin-top: 10px;
}

.action-button {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.action-button:hover {
  background: #218838;
}
</style> 