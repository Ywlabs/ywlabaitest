<template>
  <div class="about">
    <FloatingMenu />
    <div class="page-container">
      <div class="sidebar">
        <h3>회사소개</h3>
        <div class="menu-list">
          <router-link to="/about/greeting" class="menu-item">인사말</router-link>
          <router-link to="/about/history" class="menu-item">걸어온길</router-link>
          <router-link to="/about/careers" class="menu-item">채용공고</router-link>
          <router-link to="/about/location" class="menu-item">오시는길</router-link>
        </div>
      </div>
      <div class="content">
        <h1>회사소개</h1>
        <div class="about-content">
          <p>영우랩스는 혁신적인 AI 솔루션을 제공하는 기업입니다.</p>
        </div>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import FloatingMenu from '@/components/FloatingMenu.vue'
import '@/assets/layout.css'

export default {
  name: 'About',
  components: { FloatingMenu },
}
</script> 