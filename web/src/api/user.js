import request from '@/utils/request'
import { sha256 } from 'js-sha256'

export function login (username, pwd) {
  let password = sha256(pwd)
  return request.post('/auth/login', {username, password})
}

export function register (username, pwd, email) {
  let password = sha256(pwd)
  return request.post('/auth/register', {username, password, email})
}

export function getUserApi (userId) {
  return request.get('/api/v1_0/users/' + userId)
}

export function updateUserApi (userId, data) {
  return request.put('/api/v1_0/users/' + userId, data)
}

export function uploadUserPicApi (form, userId) {
  return request.put('/api/v1_0/users/' + userId + '/avatar', form)
}
