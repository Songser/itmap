import http from '@/utils/request'

function getNodes (gid) {
  return http.get('/api/v1_0/graphs/' + gid)
}
const state = {
  name: '',
  user: '',
  desc: '',
  create_date: '',
  nodes: [],
  links: [],
}

const mutations = {
  cleanNodes (state) {
    state.nodes = []
    state.links = []
  },
  setNodes (state, val) {
    state.nodes = val
  },
  setLinks (state, val) {
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
  getNodesByGraph ( {commit}, {gid}){
    getNodes(gid).then(response => {
      const data = response.data
      // commit('cleanNodes')
      data.nodes.forEach((value, index, array) => {
          commit('addNode', value.name)
      });
      data.relations.forEach((value, index, array) => {
          commit('addLink', {source: value.source, target: value.target})
      })
    })
  }
}

export default {
  state,
  mutations,
  actions
}
