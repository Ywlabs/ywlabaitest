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
    type: { type: String, default: 'info' }, // success, error, info
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
  background: #222;
  color: #fff;
  padding: 13px 28px;
  border-radius: 24px;
  font-size: 1.05em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  z-index: 9999;
  text-align: center;
  opacity: 0.97;
  pointer-events: none;
}
.common-toast.success { background: #2e7d32; }
.common-toast.error { background: #d32f2f; }
.common-toast.info { background: #2355d6; }
.fade-toast-enter-active, .fade-toast-leave-active {
  transition: opacity 0.35s;
}
.fade-toast-enter-from, .fade-toast-leave-to {
  opacity: 0;
}
</style> 