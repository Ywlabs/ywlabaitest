<template>
  <div class="esg">
    <div class="page-container">
      <div class="sidebar">
        <h3>ESG</h3>
        <div class="menu-list">
          <router-link to="/esg/compliance" class="menu-item">준법경영</router-link>
          <router-link to="/esg/environment" class="menu-item">환경경영</router-link>
          <router-link to="/esg/social" class="menu-item">사회공헌</router-link>
        </div>
      </div>
      <div class="content">
        <h1>ESG</h1>
        <div class="esg-content">
          <p>영우랩스는 지속가능한 미래를 위한 ESG 경영을 실천합니다.</p>
        </div>
        <router-view></router-view>
      </div>
    </div>
    <FloatingMenu />
  </div>
</template>

<script>
import '@/assets/layout.css'
import FloatingMenu from '@/components/FloatingMenu.vue'

export default {
  name: 'ESG',
  components: { FloatingMenu },
  // ...기존 코드...
}
</script> 