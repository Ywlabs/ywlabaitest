import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AICDMS from '@/views/solutions/AICDMS.vue'
import AIMASASIKI from '@/views/solutions/AIMASASIKI.vue'
import AIEMS from '@/views/solutions/AIEMS.vue'
import AIGENIUS from '@/views/solutions/AIGENIUS.vue'

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
        path: '',
        name: 'AboutDefault',
        redirect: '/about/greeting'
      },
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
        path: '',
        name: 'SolutionsDefault',
        redirect: '/solutions/aigenius'
      },
      {
        path: 'aigenius',
        name: 'AIGENIUS',
        component: AIGENIUS
      },
      {
        path: 'aiems',
        name: 'AIEMS',
        component: AIEMS
      },
      {
        path: 'aicdms',
        name: 'AICDMS',
        component: AICDMS
      },
      {
        path: 'aimasasiki',
        name: 'AIMASASIKI',
        component: AIMASASIKI
      }
    ]
  },
  {
    path: '/esg',
    name: 'ESG',
    component: () => import('../views/esg/ESG.vue'),
    children: [
      {
        path: '',
        name: 'ESGDefault',
        redirect: '/esg/compliance'
      },
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