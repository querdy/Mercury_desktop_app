import { createRouter, createWebHashHistory } from 'vue-router'
import ResearchView from '../views/ResearchView.vue'

const routes = [
  {
    path: '/',
    name: 'research',
    component: ResearchView
  },
  {
    path: '/vse',
    name: 'vse',
    component: () => import('../views/VSEView.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('../views/SettingsView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
