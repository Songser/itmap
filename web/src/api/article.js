import request from '@/utils/request'

export function getArticlesApi (nid) {
  return request.get('/api/v1_0/nodes/'+ nid+'/articles')
}

export function addArticleApi (nid, data) {
  return request.post('/api/v1_0/nodes/' + nid + '/articles', data)
}
