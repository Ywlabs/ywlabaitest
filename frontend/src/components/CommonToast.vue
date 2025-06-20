<template>
  <transition name="fade-toast">
    <div v-if="visible" :class="['common-toast', type]">
      {{ message }}
    </div>
  </transition>
</template>

<script>
// 공통 토스트 메시지 컴포넌트
export default {
  name: 'CommonToast',
  props: {
    message: { type: String, required: true },
    type: { type: String, default: 'info' }, // success, error, info, warning
    duration: { type: Number, default: 1800 } // ms
  },
  data() {
    return {
      visible: false,
      timer: null
    }
  },
  watch: {
    message(newVal) {
      if (newVal) this.showToast();
    }
  },
  mounted() {
    if (this.message) this.showToast();
  },
  methods: {
    showToast() {
      this.visible = true;
      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        this.visible = false;
        this.$emit('hidden');
      }, this.duration);
    }
  },
  beforeUnmount() {
    clearTimeout(this.timer);
  }
}
</script>

<style scoped>
.common-toast {
  position: fixed;
  left: 50%;
  bottom: 60px;
  transform: translateX(-50%);
  min-width: 180px;
  max-width: 80vw;
  background: #f8f9fa;
  color: #333;
  padding: 13px 28px;
  border-radius: 24px;
  font-size: 1.05em;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  z-index: 9999;
  text-align: center;
  opacity: 0.95;
  pointer-events: none;
  border: 1px solid #e9ecef;
}
.common-toast.success { 
  background: #d4edda; 
  color: #155724;
  border-color: #c3e6cb;
}
.common-toast.error { 
  background: #f8d7da; 
  color: #721c24;
  border-color: #f5c6cb;
}
.common-toast.info { 
  background: #d1ecf1; 
  color: #0c5460;
  border-color: #bee5eb;
}
.common-toast.warning { 
  background: #fff3cd; 
  color: #856404;
  border-color: #ffeaa7;
}
.fade-toast-enter-active, .fade-toast-leave-active {
  transition: opacity 0.35s;
}
.fade-toast-enter-from, .fade-toast-leave-to {
  opacity: 0;
}
</style> 