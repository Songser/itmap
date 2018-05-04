import http from '@/utils/request'

function getGraphApi (uid) {
  return http.get('/api/v1_0/users/' + uid + '/graphs')
}
const state = {
  id: 0,
  name: '',
  ownerId: 0,
  ownerName: ''
}

const mutations = {
  setGraph (state, graph) {
    state.id = graph.id
    state.name = graph.name
    state.ownerId = graph.ownerId
    state.ownerName = graph.ownerName
  },
  setGraphName (state, name) {
    state.name = name
  }
}

const actions = {
  getGraph ({commit}, uid) {
    getGraphApi(uid).then((response) => {
      commit('getGraph', response.data[0])
    })
  }
}

export default {
  state,
  mutations,
  actions
}
