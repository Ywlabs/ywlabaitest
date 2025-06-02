<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/" class="company-name">영우랩스</router-link>
      </div>
      <div class="nav-menu">
        <div class="menu-item" 
             v-for="(item, index) in menuItems" 
             :key="index"
             @mouseenter="showSubmenu(index)"
             @mouseleave="hideSubmenu(index)">
          <span class="menu-text">{{ item.name }}</span>
          <div class="submenu" v-if="item.showSubmenu">
            <router-link v-for="subItem in item.submenu" 
                        :key="subItem.path" 
                        :to="subItem.path"
                        class="submenu-item">
              {{ subItem.name }}
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      menuItems: [
        {
          name: '회사소개',
          showSubmenu: false,
          submenu: [
            { name: '인사말', path: '/about/greeting' },
            { name: '걸어온길', path: '/about/history' },
            { name: '채용공고', path: '/about/careers' },
            { name: '오시는길', path: '/about/location' }
          ]
        },
        {
          name: '솔루션',
          showSubmenu: false,
          submenu: [
            { name: 'AICDMS', path: '/solutions/aicdms' },
            { name: 'AIMASASIKI', path: '/solutions/aimasasiki' },
            { name: 'AIEMS', path: '/solutions/aiems' }
          ]
        },
        {
          name: 'ESG',
          showSubmenu: false,
          submenu: [
            { name: '준법경영', path: '/esg/compliance' },
            { name: '환경경영', path: '/esg/environment' },
            { name: '사회공헌', path: '/esg/social' }
          ]
        },
        {
          name: '문의하기',
          showSubmenu: false,
          submenu: [
            { name: '문의하기', path: '/contact' }
          ]
        }
      ]
    }
  },
  methods: {
    showSubmenu(index) {
      this.menuItems[index].showSubmenu = true
    },
    hideSubmenu(index) {
      this.menuItems[index].showSubmenu = false
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Noto Sans KR', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.company-name {
  font-size: 1.25em;
  font-weight: bold;
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  letter-spacing: 0.02em;
  transition: color 0.2s;
}
.company-name:hover {
  color: #0056b3;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.menu-item {
  position: relative;
  cursor: pointer;
  padding: 10px 0;
}

.menu-text {
  font-size: 1.1em;
  color: #2c3e50;
  transition: color 0.3s;
}

.menu-item:hover .menu-text {
  color: #42b983;
}

.submenu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  min-width: 150px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 8px 0;
  z-index: 1000;
}

.submenu-item {
  display: block;
  padding: 8px 16px;
  color: #2c3e50;
  text-decoration: none;
  transition: background-color 0.3s;
}

.submenu-item:hover {
  background-color: #f8f9fa;
  color: #42b983;
}
</style> 