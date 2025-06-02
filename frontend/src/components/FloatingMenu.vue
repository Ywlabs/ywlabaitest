<template>
  <div class="floating-menu">
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
.floating-menu {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
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