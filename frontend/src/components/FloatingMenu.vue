<template>
  <div class="floating-menu-bar">
    <button @click="navigateTo('/')" class="floating-button">영우AI</button>
  </div>
</template>

<script>
export default {
  name: 'FloatingMenu',
  methods: {
    navigateTo(url) {
      if (url) {
        this.$router.push(url)
      }
    }
  }
}
</script>

<style scoped>
.floating-menu-bar {
  position: absolute;
  right: 24px;
  bottom: 20%;
  width: auto;
  z-index: 100;
  /* 필요시 배경, 패딩 등 추가 가능 */
}

.floating-button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.floating-button:hover {
  background: #0056b3;
}
</style> 