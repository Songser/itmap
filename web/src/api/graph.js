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
  return request.post('/api/v1_0/nodes', {
    graph_id: data.graphId,
    name: data.name,
    color: data.color,
    description: data.desc,
    size: data.size,
    shape: data.shape
  })
}

export function addLinkApi (data) {
  return request.post('/api/v1_0/node_rels', {
    source_node_id: data.source_id,
    target_node_id: data.target_id,
    graph_id: data.graphId,
    info: data.value
  })
}

export function getNodesApi (gid) {
  return request.get('/api/v1_0/graphs/' + gid)
}

export function delNodeApi (id) {
  return request.delete('/api/v1_0/nodes/' + id)
}
