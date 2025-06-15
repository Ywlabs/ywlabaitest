<template>
  <div class="solutions">
    <div class="page-container">
      <div class="sidebar">
        <SideMenu>
          <h3>솔루션</h3>
          <div class="menu-list">
            <router-link to="/solutions/aigenius" class="menu-item">AIGENIUS</router-link>
            <router-link to="/solutions/aiems" class="menu-item">AIEMS</router-link>
            <router-link to="/solutions/aicdms" class="menu-item">AICDMS</router-link>
            <router-link to="/solutions/aimasasiki" class="menu-item">AIMASASIKI</router-link>
          </div>
        </SideMenu>
      </div>
      <div class="content">
        <h1>솔루션</h1>
        <div class="solutions-content">
          <p>영우랩스는 다양한 산업 분야에 최적화된 AI 솔루션을 제공합니다.</p>
        </div>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import '@/assets/layout.css'
import SideMenu from '@/components/SideMenu.vue'

export default {
  name: 'Solutions',
  components: { SideMenu }
}
</script>

<style scoped>
.solutions {
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

.solutions-content {
  margin-bottom: 2rem;
}

.solutions-content p {
  color: #666;
  line-height: 1.6;
}
</style> 