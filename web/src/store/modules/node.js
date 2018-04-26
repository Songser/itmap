const state = {
  name: 'test',
  user: '呵呵',
  desc: 'fdafsafasfasdfa',
  create_date: '2018-4-28',
  nodes: [
    {
      name: '徐贱云',
      draggable: true
    }, {
      name: '冯可梁',
      category: 1,
      draggable: true
    }, {
      name: '邓志荣',
      category: 1,
      draggable: true
    }, {
      name: '李荣庆',
      category: 1,
      draggable: true
    }, {
      name: '郑志勇',
      category: 1,
      draggable: true
    }, {
      name: '赵英杰',
      category: 1,
      draggable: true
    }, {
      name: '王承军',
      category: 1,
      draggable: true
    }, {
      name: '陈卫东',
      category: 1,
      draggable: true
    }, {
      name: '邹劲松',
      category: 1,
      draggable: true
    }, {
      name: '赵成',
      category: 1,
      draggable: true
    }, {
      name: '陈现忠',
      category: 1,
      draggable: true
    }, {
      name: '陶泳',
      category: 1,
      draggable: true
    }, {
      name: '王德福',
      category: 1,
      draggable: true
    }],
  links: [{
    source: 0,
    target: 1,
    category: 0,
    value: '朋友'
  }, {
    source: 0,
    target: 2,
    value: '战友'
  }, {
    source: 0,
    target: 3,
    value: '房东'
  }, {
    source: 0,
    target: 4,
    value: '朋友'
  }, {
    source: 1,
    target: 2,
    value: '表亲'
  }, {
    source: 0,
    target: 5,
    value: '朋友'
  }, {
    source: 4,
    target: 5,
    value: '姑姑'
  }, {
    source: 2,
    target: 8,
    value: '叔叔'
  }, {
    source: 0,
    target: 12,
    value: '朋友'
  }, {
    source: 6,
    target: 11,
    value: '爱人'
  }, {
    source: 6,
    target: 3,
    value: '朋友'
  }, {
    source: 7,
    target: 5,
    value: '朋友'
  }, {
    source: 9,
    target: 10,
    value: '朋友'
  }, {
    source: 3,
    target: 10,
    value: '朋友'
  }, {
    source: 2,
    target: 11,
    value: '同学'
  }, {
    source: 2,
    target: 13,
    value: '同学'
  }
  ]
}

const mutations = {
  setNode (state, val) {
    console.log(val)
    state.name = val.name
  },
  addNode (state, graph) {
    state.nodes.push({
      name: graph.name,
      draggable: true
    })
    state.links.push({
      source: state.node.name,
      target: graph.name,
      value: graph.name
    })
  }
}

export default {
  state,
  mutations
}
