<template>
  <header class="header">
    <nav class="nav">
      <router-link to="/" class="logo">영우랩스</router-link>
      <div class="nav-links">
        <div class="nav-item">
          <router-link to="/about" class="nav-link">회사소개</router-link>
          <div class="dropdown-content">
            <router-link to="/about/greeting">인사말</router-link>
            <router-link to="/about/history">걸어온길</router-link>
            <router-link to="/about/careers">채용공고</router-link>
            <router-link to="/about/location">오시는길</router-link>
          </div>
        </div>
        <div class="nav-item">
          <router-link to="/solutions" class="nav-link">솔루션</router-link>
          <div class="dropdown-content">
            <router-link to="/solutions/aicdms">AICDMS</router-link>
            <router-link to="/solutions/aimasasiki">AIMASASIKI</router-link>
            <router-link to="/solutions/aiems">AIEMS</router-link>
          </div>
        </div>
        <div class="nav-item">
          <router-link to="/esg" class="nav-link">ESG</router-link>
          <div class="dropdown-content">
            <router-link to="/esg/compliance">준법경영</router-link>
            <router-link to="/esg/environment">환경경영</router-link>
            <router-link to="/esg/social">사회공헌</router-link>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  data() {
    return {
      activeDropdown: null
    }
  },
  methods: {
    toggleDropdown(name) {
      this.activeDropdown = this.activeDropdown === name ? null : name
    }
  },
  watch: {
    $route() {
      this.activeDropdown = null
    }
  }
}
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-item {
  position: relative;
}

.nav-link {
  color: #2c3e50;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #42b983;
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  min-width: 200px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 4px;
  padding: 0.5rem 0;
}

.nav-item:hover .dropdown-content {
  display: block;
}

.dropdown-content a {
  color: #2c3e50;
  text-decoration: none;
  padding: 0.5rem 1rem;
  display: block;
  transition: all 0.3s;
}

.dropdown-content a:hover {
  background: #f8f9fa;
  color: #42b983;
}

.router-link-active {
  color: #42b983;
}
</style> 