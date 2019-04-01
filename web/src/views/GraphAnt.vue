<template>
  <!-- <v-graph :width="graph.width" :height="graph.width"
      :fit-view="graph.fitView" :fit-view-padding="graph.fitViewPadding"
      :animate="graph.animate" :type="graph.type"
      :layout="graph.layout"
      :data="graph.data"
      :on-afterchange="graph.onAfterchange">
      <v-node :shape="node.shape" :size="node.size" :label="node.label"></v-node>
      <v-edge :shape="edge.shape" ></v-edge>
    </v-graph> -->
    <div id='mountNode'></div>
</template>
<script>
import G6 from '@antv/g6'
import * as d3 from 'd3'
import { mapState } from 'vuex'
import { getNodesApi } from '@/api/graph'

// let Mapper = G6.Plugins['tool.d3.mapper']
let _d = d3
let forceSimulation = _d.forceSimulation
let forceLink = _d.forceLink
let forceManyBody = _d.forceManyBody
let forceX = _d.forceX
let forceY = _d.forceY
let forceCollide = _d.forceCollide
// let nodeMap = {}
// let nodeSizeMapper = new Mapper('node', 'degree', 'size', [8, 48], {
//     legendCfg: null
//   });
// let nodeColorMapper = new Mapper('node', 'type', 'color', ['#e18826', '#002a67']);
// let G = G6.G
let simulation = void 0

// let data = {
//   nodes: []
// }
let graph = new G6.Graph({
  container: 'mountNode',
  height: window.innerHeight,
  // plugins: [nodeSizeMapper, nodeColorMapper],
  modes: {
    default: ['rightPanCanvas']
  },
  layout: function layout (nodes, edges) {
    if (simulation) {
      simulation.alphaTarget(0.3).restart()
    } else {
      simulation = forceSimulation(nodes).force('charge', forceManyBody().strength(-100)).force('link', forceLink(edges).id(function (model) {
        return model.id
      })).force('collision', forceCollide().radius(function (model) {
        return model.size / 2 * 1.2
      })).force('y', forceY()).force('x', forceX()).on('tick', function () {
        graph.updateNodePosition()
      })
    }
  }
})
graph.node({
  style: (model) => {
    return {
      fill: '#002a67',
      shadowColor: 'rgba(0,0,0, 0.3)',
      shadowBlur: 3,
      shadowOffsetX: 3,
      shadowOffsetY: 5,
      stroke: null
    }
  },
  label: (model) => {
    return {
      text: model.properties['name'],
      stroke: null,
      fill: '#fff'
    }
  }
})
graph.edge({
  style: () => {
    return {
      stroke: '#b3b3b3',
      lineWidth: 2
    }
  }
})
graph.translate(graph.getWidth() / 2, graph.getHeight() / 2)

// 拖拽节点交互
let subject = void 0
graph.on('mousedown', (ev) => {
  if (ev.domEvent.button === 0) {
    subject = simulation.find(ev.x, ev.y)
  }
})
graph.on('dragstart', (ev) => {
  subject && simulation.alphaTarget(0.3).restart()
})
graph.on('mouseup', resetState)
graph.on('canvas:mouseleave', resetState)

function resetState () {
  if (subject) {
    simulation.alphaTarget(0)
    subject.fx = null
    subject.fy = null
    subject = null
  }
}
function tryHideLabel (node) {
  let model = node.getModel()
  let label = node.getLabel()
  let labelBox = label.getBBox()
  if (labelBox.maxX - labelBox.minX > model.size) {
    label.hide()
    graph.draw()
  }
}
let nodes = graph.getNodes()
let edges = graph.getEdges()
edges.forEach(function (edge) {
  edge.getGraphicGroup().set('capture', false) // 移除边的捕获，提升图形拾取效率
})
nodes.forEach(function (node) {
  tryHideLabel(node)
})
graph.on('node:mouseenter', function (ev) {
  let item = ev.item
  graph.toFront(item)
  item.getLabel().show()
  graph.draw()
})

graph.on('node:mouseleave', function (ev) {
  let item = ev.item
  tryHideLabel(item)
})
const edge = {
  shape: 'mindEdge'
}

export default {
  name: 'graph',
  data () {
    return {
      // graph,
      // node,
      edge
    }
  },
  created () {
    this.$root.eventHub.$on('addNode', target => {
    })
  },
  computed: {
    ...mapState({
      graphId: state => state.graph.id
    })
  },
  watch: {
    graphId (value) {
      if (value) {
        getNodesApi(value).then(response => {
          const data = response.data
          let nodes = []
          data.nodes.forEach((value, index, array) => {
            let node = {
              id: value.id,
              color: value.color,
              shape: value.shape,
              label: value.name,
              desc: value.description,
              create_date: value.create_date,
              index: 1
            }
            if (value.size === 'L') {
              node['size'] = [65, 65]
            } else if (value.size === 'M') {
              node['size'] = [45, 45]
            } else if (value.size === 'S') {
              node['size'] = [35, 35]
            }
            nodes.push(node)
          })
          let edges = []
          data.relations.forEach((value, index, array) => {
            let edge = {
              target: value.tid,
              source: value.sid
            }
            edges.push(edge)
          })
          this.graph.read({
            nodes: nodes,
            edges: edges
          })
          // this.data = Object.assign(
          //   {},
          //   {
          //     nodes: nodes,
          //     edges: edges
          //   }
          // );
          // this.zoom = Object.assign(
          //   {},
          //   {
          //     min: 1,
          //     max: 10,
          //     current: 1
          //   }
          // );
        })
      }
    }
  }
}
</script>
