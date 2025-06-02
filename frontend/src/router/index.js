import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/about/About.vue'),
    children: [
      {
        path: 'greeting',
        name: 'Greeting',
        component: () => import('../views/about/Greeting.vue')
      },
      {
        path: 'history',
        name: 'History',
        component: () => import('../views/about/History.vue')
      },
      {
        path: 'careers',
        name: 'Careers',
        component: () => import('../views/about/Careers.vue')
      },
      {
        path: 'location',
        name: 'Location',
        component: () => import('../views/about/Location.vue')
      }
    ]
  },
  {
    path: '/solutions',
    name: 'Solutions',
    component: () => import('../views/solutions/Solutions.vue'),
    children: [
      {
        path: 'aicdms',
        name: 'AICDMS',
        component: () => import('../views/solutions/AICDMS.vue')
      },
      {
        path: 'aimasasiki',
        name: 'AIMASASIKI',
        component: () => import('../views/solutions/AIMASASIKI.vue')
      },
      {
        path: 'aiems',
        name: 'AIEMS',
        component: () => import('../views/solutions/AIEMS.vue')
      }
    ]
  },
  {
    path: '/esg',
    name: 'ESG',
    component: () => import('../views/esg/ESG.vue'),
    children: [
      {
        path: 'compliance',
        name: 'Compliance',
        component: () => import('../views/esg/Compliance.vue')
      },
      {
        path: 'environment',
        name: 'Environment',
        component: () => import('../views/esg/Environment.vue')
      },
      {
        path: 'social',
        name: 'Social',
        component: () => import('../views/esg/Social.vue')
      }
    ]
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/contract/Contract.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 