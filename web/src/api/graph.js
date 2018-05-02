import request from '@/utils/request'

export function getFashionGraphs(){
    return request.get('/api/v1_0/graphs/fashion')
}

export function getGraphList (uid) {
    return request.get('/api/v1_0/users/' + uid + '/graphs')
}

export function addGraph (uid, name) {
    return http.post('/api/v1_0/users/'+ uid +'/graphs', {name})
}