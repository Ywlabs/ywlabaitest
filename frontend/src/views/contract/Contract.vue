<template>
  <div class="contract">
    <h1>문의하기</h1>
    <div class="contract-content">
      <p>영우랩스에 문의사항이 있으시면 아래 양식을 작성해 주세요.</p>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="author">작성자</label>
          <input type="text" id="author" v-model="form.author" required>
        </div>
        <div class="form-group">
          <label for="title">제목</label>
          <input type="text" id="title" v-model="form.title" required>
        </div>
        <div class="form-group">
          <label for="content">내용</label>
          <textarea id="content" v-model="form.content" required></textarea>
        </div>
        <button type="submit">제출</button>
      </form>
    </div>
    <FloatingMenu />
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'Contract',
  components: { FloatingMenu },
  data() {
    return {
      form: {
        title: '',
        content: '',
        author: ''
      }
    }
  },
  methods: {
    submitForm() {
      // 여기에 폼 제출 로직을 추가할 수 있습니다.
      console.log('Form submitted:', this.form)
    }
  }
}
</script>

<style scoped>
.contract {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
.contract-content {
  margin-top: 2rem;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input, textarea {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}
button {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #3aa876;
}
</style> 