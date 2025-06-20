<template>
  <div class="common-error">
    <span class="error-icon">⚠️</span>
    <span class="error-message">{{ message }}</span>
    <button v-if="retry" class="retry-btn" @click="$emit('retry')">다시 시도</button>
  </div>
</template>

<script>
// 공통 에러 메시지 컴포넌트
export default {
  name: 'CommonError',
  props: {
    message: { type: String, required: true },
    retry: { type: Boolean, default: false }
  }
}
</script>

<style scoped>
.common-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #d32f2f;
  background: #fff4f4;
  border: 1px solid #ffd6d6;
  border-radius: 8px;
  padding: 18px 16px;
  margin: 18px 0;
  font-size: 1.08em;
  gap: 8px;
}
.error-icon {
  font-size: 2em;
}
.retry-btn {
  margin-top: 8px;
  background: #fff;
  border: 1px solid #d32f2f;
  color: #d32f2f;
  border-radius: 4px;
  padding: 4px 16px;
  cursor: pointer;
  font-size: 1em;
  transition: background 0.15s, color 0.15s;
}
.retry-btn:hover {
  background: #d32f2f;
  color: #fff;
}
</style> 