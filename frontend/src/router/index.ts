import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import About from '../views/about/About.vue'
import Greeting from '../views/about/Greeting.vue'
import History from '../views/about/History.vue'
import Careers from '../views/about/Careers.vue'
import Location from '../views/about/Location.vue'
import Solutions from '../views/solutions/Solutions.vue'
import AIGENIUS from '../views/solutions/AIGENIUS.vue'
import AIEMS from '../views/solutions/AIEMS.vue'
import AICDMS from '../views/solutions/AICDMS.vue'
import AIMASASIKI from '../views/solutions/AIMASASIKI.vue'
import ESG from '../views/esg/ESG.vue'
import Compliance from '../views/esg/Compliance.vue'
import Environment from '../views/esg/Environment.vue'
import Social from '../views/esg/Social.vue'
import Contract from '../views/contract/Contract.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    children: [
      { path: '', name: 'AboutDefault', redirect: '/about/greeting' },
      { path: 'greeting', name: 'Greeting', component: Greeting },
      { path: 'history', name: 'History', component: History },
      { path: 'careers', name: 'Careers', component: Careers },
      { path: 'location', name: 'Location', component: Location }
    ]
  },
  {
    path: '/solutions',
    name: 'Solutions',
    component: Solutions,
    children: [
      { path: '', name: 'SolutionsDefault', redirect: '/solutions/aigenius' },
      { path: 'aigenius', name: 'AIGENIUS', component: AIGENIUS },
      { path: 'aiems', name: 'AIEMS', component: AIEMS },
      { path: 'aicdms', name: 'AICDMS', component: AICDMS },
      { path: 'aimasasiki', name: 'AIMASASIKI', component: AIMASASIKI }
    ]
  },
  {
    path: '/esg',
    name: 'ESG',
    component: ESG,
    children: [
      { path: '', name: 'ESGDefault', redirect: '/esg/compliance' },
      { path: 'compliance', name: 'Compliance', component: Compliance },
      { path: 'environment', name: 'Environment', component: Environment },
      { path: 'social', name: 'Social', component: Social }
    ]
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contract
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: { template: '<div>관리자 페이지(임시)</div>' }, // 실제 구현 전 임시 컴포넌트
    meta: { requiresAdmin: true },
    children: [
      {
        path: 'usermgt',
        name: 'AdminUserMgt',
        component: { template: '<div>사용자 관리(임시)</div>' },
        meta: { requiresAdmin: true }
      }
      // 추후 하위 관리자 메뉴 추가 가능
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 인증/권한 라우트 가드 (한글 주석 포함)
router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const token = localStorage.getItem('jwt_token');
  const user = JSON.parse(localStorage.getItem('user_info') || 'null');
  const userRole = user?.role;

  // 인증 필요
  if (authRequired && !token) {
    return next('/login');
  }
  // 로그인 상태에서 /login 접근 시 홈으로 리다이렉트
  if (to.path === '/login' && token) {
    return next('/');
  }
  // admin 권한 필요: /admin 및 하위 경로 전체
  if (to.matched.some(record => record.meta.requiresAdmin) && userRole !== 'admin') {
    return next('/'); // 또는 '/403' 등
  }
  next();
});

export default router 