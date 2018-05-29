import Vue from 'vue'
import VueRouter from 'vue-router'
import http from '@/utils/request'
import store from '@/store'
import Graph from '@/components/Graph'
import Layout from '@/layout/Layout'
import Login from '@/components/Login'
import Register from '@/components/Register'
import User from '@/components/User'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Layout,
      children: [{
        path: 'index',
        component: Graph,
        name: 'index'
      }]
    },
    {
      path: '/graph',
      name: 'Graph',
      component: Graph
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/user',
      name: 'User',
      component: User
    }
  ]
})

function getUser () {
  return http.get('/auth/current_user')
}

router.beforeResolve((to, from, next) => {
  if (!store.state.user.id) {
    getUser().then(response => {
      store.commit('setUser', response.data)
      next()
    }, response => {
      console.error(response)
      next()
    })
  } else {
    next()
  }
})

export default router
