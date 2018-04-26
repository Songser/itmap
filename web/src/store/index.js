import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import node from './modules/node'
import graph from './modules/graph'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    node,
    graph
  }
})
