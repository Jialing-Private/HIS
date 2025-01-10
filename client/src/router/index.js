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
      // 添加click操作后的界面跳转途径（开始处）
      {
        path: '/preLog',
        name: 'preLog',
        component: require('../views/preLog.vue').default
      },
      {
        path: '/resLog',
        name: 'resLog',
        component: require('../views/resLog.vue').default
      },
      {
        path: '/opd_diagnosis',
        name: 'opd_diagnosis',
        component: require('../views/opd_diagnosis.vue').default
      }
      // 添加click操作后的界面跳转途径（结束处）
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router