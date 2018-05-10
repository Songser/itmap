import {
  addNodeApi,
  addLinkApi,
  getNodesApi,
  delNodeApi
} from '@/api/graph'

const state = {
  id: 0,
  name: '',
  desc: '',
  create_date: '',
  nodes: [],
  links: []
}

const mutations = {
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
  addNode (state, value) {
    let node = {
      nid: value.target_id,
      name: value.name,
      desc: value.desc,
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
    state.nodes.push(node)
  },
  addLink (state, {source, target, value}) {
    state.links.push({
      source,
      target,
      value
    })
  },
  delNode (state, name) {
    let nodes = []
    let links = []
    for (let n of state.nodes) {
      if (name !== n.name) {
        nodes.push(n)
      }
    }
    for (let l of state.links) {
      if (name !== l.source || name !== l.target) {
        links.push(l)
      }
    }
    state.nodes = nodes
    state.links = links
  }
}

const actions = {
  getNodesByGraph ({commit}, {gid}) {
    getNodesApi(gid).then(response => {
      const data = response.data
      commit('setGraph', {id: data.id,
        name: data.name,
        ownerId: data.owner_id,
        ownerName: data.owner_name
      })
      commit('setLinks', data.relations)
      commit('setNodes', data.nodes)
      if (data.nodes.length > 0) {
        commit('setNode', data.nodes[0])
      } else {
        commit('setNode', {
          id: 0,
          name: '',
          desc: '',
          create_date: ''
        })
      }
      return data.id
    })
  },
  addNode ({commit}, data) {
    addNodeApi(data).then(response => {
      data['target_id'] = response.data
      commit('addNode', data)
      let upload = data.upload
      data.action = BASE_URL + '/api/v1_0/nodes/' + data['target_id'] + '/pic'
      upload.submit()
      if (data.source && data.target) {
        addLinkApi(data).then(response => {
          commit('addLink', {
            source: data.source,
            target: data.target,
            value: data.value
          })
          
        })
      }
      return data['target_id']
    })
  },
  delNode ({commit}, {id, name}) {
    delNodeApi(id).then(response => {
      commit('delNode', name)
    })
  }
}

export default {
  state,
  mutations,
  actions
}
