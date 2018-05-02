import request from '@/utils/request'
import { sha256 } from 'js-sha256'

export function login (username, pwd) {
    let password = sha256(pwd)
    return request.post('/auth/login', {username, password})
}

function register (username, pwd, email) {
    let password = sha256(pwd)
    return http.post('/auth/register', {username, password, email})
}