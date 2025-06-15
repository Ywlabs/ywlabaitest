<template>
  <div class="contract">
    <div class="page-container">
      <div class="sidebar">
        <SideMenu>
          <h3>고객센터</h3>
          <div class="menu-list">
            <a href="#" class="menu-item router-link-active">고객센터 안내</a>
          </div>
        </SideMenu>
      </div>
      <div class="content">
        <h1>고객센터 안내</h1>
        <section class="contact-guide">
          <p>
            영우랩스는 고객님의 문의에 친절하고 신속하게 답변드리겠습니다.<br>
            문의하실 내용과 연락처를 남겨주시면 담당자가 빠르게 안내해드립니다.
          </p>
        </section>
        <section class="contact-hours">
          <h2>고객센터 근무시간</h2>
          <ul>
            <li>평일 09:00 ~ 18:00 (점심시간 12:00 ~ 13:00)</li>
            <li>주말/공휴일 휴무</li>
          </ul>
        </section>
        <section class="contact-managers">
          <h2>업무별 담당자 연락처</h2>
          <ul>
            <li><strong>영업문의</strong>: 010-1234-5678 / sales@ywlabs.com</li>
            <li><strong>기술지원</strong>: 010-2345-6789 / support@ywlabs.com</li>
            <li><strong>일반문의</strong>: 010-3456-7890 / info@ywlabs.com</li>
          </ul>
        </section>
        <section id="contact-form" class="contact-form-section">
          <h2>고객문의하기</h2>
          <div class="contract-content">
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
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import SideMenu from '@/components/SideMenu.vue'
export default {
  name: 'Contract',
  components: { SideMenu },
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
  min-height: 100vh;
  padding-top: 80px;
}
.page-container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 80px);
}
.sidebar {
  width: 250px;
  background: #fff;
  border-right: 1px solid #eee;
  height: 100%;
  position: fixed;
  left: 0;
  top: 80px;
  z-index: 100;
}
.sidebar h3 {
  font-size: 1.15em;
  font-weight: bold;
  margin: 1.5rem 0 1rem 0;
  color: #2c3e50;
  border-bottom: 3px solid #42b983;
  padding-bottom: 0.5rem;
  width: 90%;
}
.content {
  flex: 1;
  margin-left: 250px;
  padding: 2rem;
  max-width: 950px;
  margin-right: auto;
}
.menu-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
}
.menu-item {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
  font-weight: 500;
  display: block;
  width: 100%;
  text-align: left;
  box-sizing: border-box;
}
.menu-item:hover {
  background: #f8f9fa;
  color: #42b983;
}
.menu-item.router-link-active,
.menu-item.router-link-exact-active {
  background: #42b983;
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(66,185,131,0.08);
}
.contact-guide {
  margin-bottom: 2rem;
  font-size: 1.1em;
  color: #333;
}
.contact-hours {
  margin-bottom: 2rem;
}
.contact-hours h2 {
  font-size: 1.1em;
  color: #2355d6;
  margin-bottom: 0.5rem;
}
.contact-hours ul {
  list-style: disc inside;
  color: #444;
  margin-left: 1.2em;
}
.contact-managers {
  margin-bottom: 2rem;
}
.contact-managers h2 {
  font-size: 1.1em;
  color: #2355d6;
  margin-bottom: 0.5rem;
}
.contact-managers ul {
  list-style: disc inside;
  color: #444;
  margin-left: 1.2em;
}
.contact-form-section {
  margin-bottom: 2rem;
}
.contract-content {
  margin-top: 1rem;
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