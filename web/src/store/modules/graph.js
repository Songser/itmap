import http from '@/utils/request'

function getMainGraph () {
  return http.get('/api/v1_0/graphs')
}
const state = {
  id: 0,
  name: '',
  ownerId: 0
}

const mutations = {
  getGraph (state, {id, name, ownerId}) {
    state.id = id
    state.name = name
    state.ownerId = ownerId
  }
}

const actions = {
  getGraph ({commit}) {
    getMainGraph().then((response) => {
      commit('getGraph', response.data[0])
    })
  }
}

export default {
  state,
  mutations,
  actions
}
