<template>
  <div class="login-page">
    <div class="login-box">
      <h2>로그인</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">이메일</label>
          <input v-model="email" id="email" type="email" required autocomplete="username" />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input v-model="password" id="password" type="password" required autocomplete="current-password" />
        </div>
        <button type="submit" :disabled="loading">로그인</button>
      </form>
      <CommonLoading v-if="loading" message="로그인 중..." />
      <CommonError v-if="errorMessage" :message="errorMessage" @retry="handleLogin" />
      <CommonToast v-if="toastMessage" :message="toastMessage" type="error" @hidden="toastMessage = ''" />
    </div>
  </div>
</template>

<script>
import api from '@/common/axios'
import CommonLoading from '@/components/CommonLoading.vue'
import CommonError from '@/components/CommonError.vue'
import CommonToast from '@/components/CommonToast.vue'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'Login',
  components: { CommonLoading, CommonError, CommonToast },
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      errorMessage: '',
      toastMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = '';
      this.toastMessage = '';
      try {
        const res = await api.post('/api/auth/login', {
          email: this.email,
          password: this.password
        });
        if (!res.data.success) {
          this.toastMessage = res.data.message || '로그인에 실패했습니다.';
          return;
        }
        const authStore = useAuthStore();
        authStore.login(res.data.data.token, res.data.data.user);
        this.$router.push('/');
      } catch (e) {
        this.toastMessage = e.response?.data?.message || '로그인 중 오류가 발생했습니다.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f8fb;
}
.login-box {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  padding: 36px 32px 28px 32px;
  min-width: 320px;
  max-width: 380px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.login-box h2 {
  margin-bottom: 18px;
  color: #2355d6;
  font-size: 1.3em;
  font-weight: bold;
}
.form-group {
  width: 100%;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
label {
  font-size: 0.98em;
  color: #555;
  margin-bottom: 4px;
}
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #bbb;
  border-radius: 5px;
  font-size: 1em;
  margin-bottom: 2px;
}
button[type="submit"] {
  width: 100%;
  padding: 10px 0;
  background: #2355d6;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 1.08em;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.18s;
}
button[type="submit"]:hover {
  background: #1a3e8a;
}
</style> 