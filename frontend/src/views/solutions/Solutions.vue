<template>
  <div class="solutions">
    <div class="page-container">
      <div class="sidebar">
        <h3>솔루션</h3>
        <div class="menu-list">
          <router-link to="/solutions/aicdms" class="menu-item">AICDMS</router-link>
          <router-link to="/solutions/aimasasiki" class="menu-item">AIMASASIKI</router-link>
          <router-link to="/solutions/aiems" class="menu-item">AIEMS</router-link>
        </div>
      </div>
      <div class="content">
        <h1>솔루션</h1>
        <div class="solutions-content">
          <p>영우랩스는 다양한 산업 분야에 최적화된 AI 솔루션을 제공합니다.</p>
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
  name: 'Solutions',
  components: { FloatingMenu },
  // ...기존 코드...
}
</script> 