import request from '@/utils/request'

export function getFashionGraphs () {
  return request.get('/api/v1_0/graphs/fashion')
}

export function getGraphList (uid) {
  return request.get('/api/v1_0/users/' + uid + '/graphs')
}

export function addGraph (uid, name) {
  return request.post('/api/v1_0/users/' + uid + '/graphs', {name})
}

export function addNodeApi (data) {
  console.log(data)
  return request.post('/api/v1_0/nodes', {
    graph_id: data.graphId,
    name: data.name,
    color: data.color,
    description: data.desc
  })
}
