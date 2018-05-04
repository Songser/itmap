import http from '@/utils/request'
import { addNodeApi, addLinkApi } from '@/api/graph'

function getNodes (gid) {
  return http.get('/api/v1_0/graphs/' + gid)
}
const state = {
  id: 0,
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
    val.forEach((value, index, array) => {
      let node = {
        name: value.name,
        nid: value.id,
        desc: value.description,
        create_date: value.create_date
      }
      if (value.color) {
        node['itemStyle'] = { 'color': value.color }
      }
      if (value.size === 'L') {
        node['symbolSize'] = [65, 65]
      } else if (value.size === 'M') {
        node['symbolSize'] = [45, 45]
      } else if (value.size === 'S') {
        node['symbolSize'] = [35, 35]
      }
      if (value.shape) {
        node['symbol'] = value.shape
      }
      nodes.push(node)
    })
    state.nodes = nodes
  },
  setLinks (state, val) {
    state.links = val
  },
  setNode (state, val) {
    state.id = val.id
    state.name = val.name
    state.desc = val.description
    state.create_date = val.create_date
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
  addNode (state, value) {
    let node = {name: value.name}
    if (value.color) {
      node['itemStyle'] = { 'color': value.color }
    }
    if (value.size === 'L') {
      node['symbolSize'] = [65, 65]
    } else if (value.size === 'M') {
      node['symbolSize'] = [45, 45]
    } else if (value.size === 'S') {
      node['symbolSize'] = [35, 35]
    }
    if (value.shape) {
      node['symbol'] = value.shape
    }
    state.nodes.push(node)
  },
  addLink (state, {source, target, value}) {
    state.links.push({
      source,
      target,
      value
    })
  }
}

const actions = {
  getNodesByGraph ({commit}, {gid}) {
    getNodes(gid).then(response => {
      const data = response.data
      commit('setGraph', {id: data.id,
        name: data.name,
        ownerId: data.owner_id,
        ownerName: data.owner_name
      })
      commit('setLinks', data.relations)
      commit('setNodes', data.nodes)
      commit('setNode', data.nodes[0])
    })
  },
  addNode ({commit}, data) {
    addNodeApi(data).then(response => {
      commit('addNode', data)
      data['target_id'] = response.data
      addLinkApi(data).then(response => {
        commit('addLink', {
          source: data.source,
          target: data.target,
          value: data.value
        })
      })
    })
  }
}

export default {
  state,
  mutations,
  actions
}
