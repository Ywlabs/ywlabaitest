<template>
  <div class="about">
    <div class="page-container">
      <div class="sidebar">
        <SideMenu>
          <h3>회사소개</h3>
          <div class="menu-list">
            <router-link to="/about/greeting" class="menu-item">인사말</router-link>
            <router-link to="/about/history" class="menu-item">연혁</router-link>
            <router-link to="/about/careers" class="menu-item">채용정보</router-link>
            <router-link to="/about/location" class="menu-item">오시는 길</router-link>
          </div>
        </SideMenu>
      </div>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import '@/assets/layout.css'
import SideMenu from '@/components/SideMenu.vue'

export default {
  name: 'About',
  components: { SideMenu }
}
</script>

<style scoped>
.about {
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

.about-footer {
  margin-top: 3rem;
  text-align: center;
  color: #666;
  font-size: 0.98em;
}
.about-footer hr {
  margin: 2rem 0 1rem 0;
  border: none;
  border-top: 1px solid #eee;
}
.company-info {
  margin-bottom: 1rem;
}
.copyright {
  display: block;
  margin-top: 0.5rem;
  color: #aaa;
  font-size: 0.95em;
}
</style> 