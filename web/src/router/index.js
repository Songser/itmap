import Vue from 'vue'
import VueRouter from 'vue-router'
import http from '@/utils/request'
import store from '@/store'
import Layout from '@/layout/Layout'
import AppHeader from '@/views/AppHeader'
import Login from '@/views/Login'
import Register from '@/views/Register'


Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Layout,
      children: [{
        path: 'index',
        component: AppHeader,
        name: 'index'
      }]
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
