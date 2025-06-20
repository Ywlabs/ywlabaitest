import { defineStore } from 'pinia'

// 인증 상태 관리 스토어
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('jwt_token') || '',
    user: JSON.parse(localStorage.getItem('user_info') || 'null'),
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    // 로그인: 토큰/유저정보 저장
    login(token, user) {
      this.token = token
      this.user = user
      localStorage.setItem('jwt_token', token)
      localStorage.setItem('user_info', JSON.stringify(user))
    },
    // 로그아웃: 토큰/유저정보 삭제
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('user_info')
    },
    // 유저 정보 갱신
    setUser(user) {
      this.user = user
      localStorage.setItem('user_info', JSON.stringify(user))
    }
  }
}) 