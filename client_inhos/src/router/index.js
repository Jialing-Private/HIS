import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'index',
    component: require('../views/index.vue').default,
    children: [
      {
        path: '/welcome',
        name: 'welcome',
        component: require('../views/welcome.vue').default
      },
      {
        path: '/list',
        name: 'list',
        component: require('../views/list.vue').default
      },
      {
        path: '/user',
        name: 'user',
        component: require('../views/user.vue').default
      },
      {
        path: '/inhos',
        name: 'inhos',
        component: require('../views/inhos.vue').default
      },
      
      {
        path: '/doctor_inhos',
        name: 'doctor_inhos',
        component: require('../views/doctor_inhos.vue').default
      },

      {
        path: '/doctor_info',
        name: 'doctor_info',
        component: require('../views/doctor_info.vue').default
      },

      {
        path: '/preLog',
        name: 'preLog',
        component: require('../views/preLog.vue').default
      },
      {
        path: '/opd_diagnosis',
        name: 'opd_diagnosis',
        component: require('../views/opd_diagnosis.vue').default
      }

    ]
  }
]

const router = new VueRouter({
  routes
})

export default router