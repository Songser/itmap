import Vue from 'vue'
import Router from 'vue-router'
import Graph from '@/components/Graph'
import Layout from '@/layout/Layout'
import Login from '@/components/Login'
import Register from '@/components/Register'

Vue.use(Router)

export default new Router({
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
    }
  ]
})
