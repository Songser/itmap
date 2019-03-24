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
  setUser (state, data) {
    state.id = data.user_id
    state.name = data.name
    state.email = data.email
    state.active = data.active
    state.avatar = process.env.BASE_API + '/avatars/' + data.avatar
  },
  setUserAvatar (state, avatar) {
    state.avatar = process.env.BASE_API + '/avatars/' + avatar
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
