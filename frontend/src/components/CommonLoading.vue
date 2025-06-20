<template>
  <div class="common-loading">
    <span class="spinner"></span>
    <span v-if="message" class="loading-message">{{ message }}</span>
  </div>
</template>

<script>
// 공통 로딩 스피너 컴포넌트
export default {
  name: 'CommonLoading',
  props: {
    message: { type: String, default: '' }
  }
}
</script>

<style scoped>
.common-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 18px 0;
  color: #2355d6;
}
.spinner {
  width: 36px;
  height: 36px;
  border: 4px solid #e0e6ef;
  border-top: 4px solid #2355d6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 4px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-message {
  font-size: 1.08em;
  color: #2355d6;
}
</style> 