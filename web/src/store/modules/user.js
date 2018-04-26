import { getToken } from '@/utils/auth'

const state = {
  id: 0,
  name: '',
  email: '',
  active: false,
  token: getToken(),
  avatar: ''
}

const mutations = {
  setUser (state, {userId, name, email, active}) {
    state.id = userId
    state.name = name
    state.email = email
    state.active = active
  }
}

const getters = {
  token: state => state.token
}

export default {
  state,
  mutations,
  getters
}
