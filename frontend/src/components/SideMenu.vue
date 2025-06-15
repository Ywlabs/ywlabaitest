<template>
  <div class="side-menu">
    <div class="menu-list">
      <slot></slot>
    </div>
    <div class="bottom-section">
      <div class="ywoo-ai-button">
        <button @click="navigateTo('/')" class="floating-button">
          <i class="fas fa-headset"></i>
          <span>AI고객센터</span>
        </button>
      </div>
      <div class="company-info">
        <p class="company-name">주식회사 영우랩스</p>
        <p class="contact-info">
          <span>주소: 서울특별시 강동구 고덕비즈밸리로 26 A동 1513호</span>
          <span>대표전화: 010-6247-3959</span>
          <span>이메일: amma76@ywlabs.com</span>
        </p>
        <p class="copyright">© 2024 YWLABS. All rights reserved With AI</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SideMenu',
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
.side-menu {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 1rem;
  position: relative;
}

.menu-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 3rem;
}

.bottom-section {
  margin-top: auto;
  border-top: 1px solid #eee;
  padding: 1rem;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 250px;
  background: white;
  z-index: 1000;
  box-sizing: border-box;
}

.ywoo-ai-button {
  margin-bottom: 1rem;
  padding: 0 0.5rem;
}

.floating-button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.floating-button i {
  font-size: 1.1em;
}

.floating-button:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.company-info {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  padding: 0 0.5rem;
}

.company-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  padding: 0 0.5rem;
}

.contact-info span {
  display: block;
  text-align: center;
}

.copyright {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #999;
  text-align: center;
}

@media (max-height: 800px) {
  .menu-list {
    margin-bottom: 2.5rem;
  }
  
  .bottom-section {
    padding: 0.8rem;
  }
  
  .ywoo-ai-button {
    margin-bottom: 0.8rem;
  }
  
  .company-info {
    font-size: 0.7rem;
  }
  
  .contact-info {
    gap: 0.2rem;
  }
  
  .copyright {
    font-size: 0.65rem;
    margin-top: 0.3rem;
  }
}
</style> 