import http from '@/utils/request'

function getMainGraph () {
  return http.get('/api/v1_0/graphs')
}
const state = {
  id: 0,
  name: '',
  owner_id: 0
}

const mutations = {
  getGraph (state, {id, name, owner_id}) {
    state.id = id
    state.name = name
    state.owner_id = owner_id
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
