import http from '@/utils/request'

function getNodes (gid) {
  return http.get('/api/v1_0/graphs/' + gid + '/nodes')
}
const state = {
  name: 'test',
  user: '呵呵',
  desc: 'fdafsafasfasdfa',
  create_date: '2018-4-28',
  nodes: [],
  links: [],
}

const mutations = {
  setNodes (state, val) {
    console.log(state.nodes)
    console.log(val)
    state.nodes = val
    console.log(state.nodes)
  },
  setLinks (state, val) {
    console.log(val)
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
      console.log(response.data)
      data.nodes.forEach((value, index, array) => {
          commit('addNode', value.name)
      });
      data.links.forEach((value, index, array) => {
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
