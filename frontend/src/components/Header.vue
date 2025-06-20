<template>
  <header class="header">
    <nav class="nav">
      <router-link to="/" class="logo">
        <img src="/assets/img/logo.png" alt="영우랩스 로고" class="logo-img" />
      </router-link>
      <div class="nav-links">
        <!-- 로그인 상태일 때만 전체 메뉴 노출 -->
        <template v-if="isAuthenticated">
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
        </template>
        
        <!-- 관리자 메뉴 (admin role일 때만 노출) -->
        <div v-if="isAuthenticated && userRole === 'admin'" class="nav-item">
          <router-link to="/admin" class="nav-link">관리자</router-link>
        </div>

        <!-- 로그인/사용자 정보 -->
        <div v-if="isAuthenticated" class="nav-item user-info">
          <div class="user-details">
            <span class="user-email">{{ userEmail }}</span>
            <span v-if="hasEmployeeId" class="user-name">{{ displayName }}</span>
            <span v-if="userRole === 'user' && !hasEmployeeId" class="mapping-notice">직원정보 매핑필요</span>
            <span v-if="userRole === 'admin'" class="admin-notice">({{ userName }})</span>
          </div>
          <button class="logout-btn" @click="handleLogout">로그아웃</button>
        </div>
        <div v-else class="nav-item">
          <router-link to="/login" class="nav-link">로그인</router-link>
        </div>
      </div>
    </nav>
    
    <!-- 토스트 메시지 -->
    <CommonToast 
      :message="toastMessage" 
      :type="toastType" 
      :show="showToast"
      @close="showToast = false"
    />
  </header>
</template>

<script>
import { useAuthStore } from '@/store/auth'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import CommonToast from './CommonToast.vue'

export default {
  name: 'Header',
  components: {
    CommonToast
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    // 토스트 상태
    const toastMessage = ref('')
    const toastType = ref('info')
    const showToast = ref(false)
    
    // 인증 여부, 사용자명, 역할
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const userRole = computed(() => authStore.user?.role || '')
    const hasEmployeeId = computed(() => authStore.user?.employee_id !== null)
    
    // 표시할 이름 (직원명/직책 또는 이메일)
    const displayName = computed(() => {
      const user = authStore.user
      console.log('Header - User info:', user) // 디버깅용
      
      if (user?.employee_name) {
        // 직원명과 직책이 모두 있으면 "직원명 / 직책" 형태로 표시
        if (user.employee_position) {
          return `${user.employee_name} / ${user.employee_position}`
        }
        return user.employee_name // 직책이 없으면 직원명만
      }
      return user?.email || user?.name || '' // 직원 정보가 없으면 이메일 또는 이름
    })
    
    // 사용자 이메일
    const userEmail = computed(() => {
      const user = authStore.user
      return user?.email || ''
    })
    
    // 사용자 이름
    const userName = computed(() => {
      const user = authStore.user
      return user?.name || user?.email?.split('@')[0] || ''
    })
    
    // 토스트 표시 함수
    const showToastMessage = (message, type = 'info') => {
      toastMessage.value = message
      toastType.value = type
      showToast.value = true
      
      // 3초 후 자동으로 토스트 숨기기
      setTimeout(() => {
        showToast.value = false
      }, 3000)
    }
    
    // 로그아웃 함수
    const handleLogout = () => {
      authStore.logout()
      showToastMessage('로그아웃이 완료되었습니다.', 'success')
      
      // 토스트 메시지 표시 후 로그인 페이지로 이동
      setTimeout(() => {
        router.push('/login')
      }, 1000)
    }
    
    return { 
      isAuthenticated, 
      displayName, 
      userRole, 
      handleLogout,
      toastMessage,
      toastType,
      showToast,
      hasEmployeeId,
      userEmail,
      userName
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
  width: 100%;
  box-sizing: border-box;
  max-width: 1400px;
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

.user-info {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.2rem;
}

.user-name {
  color: #2355d6;
  font-weight: 600;
  font-size: 0.85em;
}

.user-email {
  color: #666;
  font-weight: 500;
  font-size: 0.85em;
}

.mapping-notice {
  color: #dc3545;
  font-size: 0.75em;
  font-weight: 500;
  line-height: 1;
  text-align: right;
}

.admin-notice {
  color: #2355d6;
  font-size: 0.75em;
  font-weight: 500;
  line-height: 1;
  text-align: right;
}

.logout-btn {
  background: #f4f8fb;
  color: #2355d6;
  border: 1px solid #2355d6;
  border-radius: 5px;
  padding: 4px 12px;
  font-size: 0.98em;
  cursor: pointer;
  transition: background 0.18s;
}
.logout-btn:hover {
  background: #2355d6;
  color: #fff;
}
</style> 