import http from '@/utils/request'
import { addNodeApi } from '@/api/graph'

function getNodes (gid) {
  return http.get('/api/v1_0/graphs/' + gid)
}
const state = {
  name: '',
  desc: '',
  create_date: '',
  nodes: [],
  links: []
}

const mutations = {
  cleanNodes (state) {
    state.nodes = []
    state.links = []
  },
  setNodes (state, val) {
    let nodes = []
    console.log(val)
    val.forEach((value, index, array) => {
      nodes.push({'name': value.name})
    })
    state.nodes = nodes
  },
  setLinks (state, val) {
    let links = []
    state.links = val
  },
  setNode (state, val) {
    state.name = val.name
  },
  addNodes (state, graph) {
    state.nodes.push({
      name: graph.name
    })
    state.links.push({
      source: state.node.name,
      target: graph.name,
      value: graph.name
    })
  },
  addNode (state, name) {
    state.nodes.push({
      name
    })
  },
  addLink (state, {source, target}) {
    state.links.push({
      source,
      target,
      value: ''
    })
  }
}

const actions = {
  getNodesByGraph ({commit}, {gid}) {
    getNodes(gid).then(response => {
      const data = response.data
      commit('setLinks', data.relations)
      commit('setNodes', data.nodes)
    })
  },
  addNode ({commit}, data) {
    addNodeApi(data).then(response => {
      console.log('dddddd')
    })
  }
}

export default {
  state,
  mutations,
  actions
}
