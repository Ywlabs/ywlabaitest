<template>
  <header class="header">
    <nav class="nav">
      <router-link to="/" class="logo">
        <img src="/assets/img/logo.png" alt="영우랩스 로고" class="logo-img" />
      </router-link>
      <div class="nav-links">
        <div class="nav-item">
          <a href="/about" class="nav-link">회사소개</a>
          <div class="dropdown-content">
            <router-link to="/about/greeting">인사말</router-link>
            <router-link to="/about/history">걸어온길</router-link>
            <router-link to="/about/careers">채용공고</router-link>
            <router-link to="/about/location">오시는길</router-link>
          </div>
        </div>
        <div class="nav-item">
          <a href="/solutions" class="nav-link">솔루션</a>
          <div class="dropdown-content">
            <router-link to="/solutions/aigenius">AIGENIUS</router-link>
            <router-link to="/solutions/aiems">AIEMS</router-link>
            <router-link to="/solutions/aicdms">AICDMS</router-link>
            <router-link to="/solutions/aimasasiki">AIMASASIKI</router-link>
          </div>
        </div>
        <div class="nav-item">
          <a href="/esg" class="nav-link">ESG</a>
          <div class="dropdown-content">
            <router-link to="/esg/compliance">준법경영</router-link>
            <router-link to="/esg/environment">환경경영</router-link>
            <router-link to="/esg/social">사회공헌</router-link>
          </div>
        </div>
        <div class="nav-item">
          <a href="/contact" class="nav-link">문의하기</a>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header'
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
  width: 100%;
  box-sizing: border-box;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 0 1rem 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  margin: 0;
}

.logo-img {
  height: 36px;
  vertical-align: middle;
}

.nav-links {
  display: flex;
  gap: 2.5rem;
  align-items: center;
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
  cursor: pointer;
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
  z-index: 1001;
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
  font-weight: 600;
}
</style> 