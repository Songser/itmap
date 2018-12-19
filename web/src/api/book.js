import request from '@/utils/request'

export function getBooksApi (nid, page) {
  return request.get('/api/v1_0/nodes/'+ nid+'/books?page=' + page)
}

export function addBookApi (nid, data) {
  return request.post('/api/v1_0/nodes/' + nid + '/books', data)
}

export function uploadBookPicApi (form, bookId) {
  return request.post('/api/v1_0/books/' + bookId + '/pic', form)
}
