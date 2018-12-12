import request from '@/utils/request'

export function getCommentsApi (nid, page) {
  return request.get('/api/v1_0/nodes/'+ nid+'/comments?page=' + page)
}

export function addCommentApi (nid, data) {
  return request.post('/api/v1_0/nodes/' + nid + '/comments', data)
}
