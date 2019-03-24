<template>
  <div class="main-graph">
    <chart ref="graph" :options="graph" @click="clickNode"/>
  </div>
</template>

<style scoped>
.main-graph {
  height: 100%;
  width: 100%;
  margin: 0px;
  padding: 0px;
}
.echarts {
  height: 95%;
  width: 100%;
  margin: 10px;
  padding: 0px;
}
</style>

<script>
import { mapState } from 'vuex'
import ECharts from 'vue-echarts/components/ECharts'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/graph'
import 'echarts/lib/component/tooltip'
import {getNodesApi} from '@/api/graph'

export default {
  name: 'graph',
  components: {
    chart: ECharts
  },
  computed: {
    ...mapState({
      graphId: state => state.graph.id,
      node: state => state.node
    })
  },
  created () {
    this.$root.eventHub.$on('addNode', (target) => {
      this.addNode(target)
    })
    this.$root.eventHub.$on('addLink', (target) => {
      this.addLink(target)
    })
    this.$root.eventHub.$on('delNode', (target) => {
      this.delNode(target)
    })
    this.$root.eventHub.$on('updateNode', (target) => {
      this.updateNode(target)
    })
  },
  data: function () {
    return {
      oldGraphId: 0,
      graph: {
        title: {
          text: 'test'
        },
        left: '10%',
        top: 'auto',
        right: 'auto',
        bottom: 'auto',
        width: 800,
        height: 900,
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        edgeSymbol: ['circle', 'arrow'],
        label: {
          normal: {
            show: true,
            textStyle: {
              fontSize: 12
            }
          }
        },
        legend: {
          x: 'center',
          show: false,
          data: ['朋友', '战友', '亲戚']
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            symbolSize: 45,
            focusNodeAdjacency: true,
            roam: true,
            draggable: true,
            categories: [],
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontsize: 12
                }
              }
            },
            force: {
              repulsion: 1000
            },
            edgeSymbolSize: [4, 50],
            edgeLabel: {
              normal: {
                show: true,
                textStyle: {
                  fontSize: 10
                },
                formatter: '{c}'
              }
            },
            data: [],
            links: [],
            lineStyle: {
              normal: {
                opacity: 0.9,
                width: 1,
                curveness: 0
              }
            }
          }
        ]
      }
    }
  },
  watch: {
    graphId (value) {
      if (value) {
        if (this.oldGraphId === value) {
          return
        }
        this.oldGraphId = value
        getNodesApi(value).then(response => {
          const data = response.data
          if (data.nodes.length === 0) {
            this.updateGraph([], [])
            this.$root.eventHub.$emit('addNodeEvent', '')
            return
          }

          let nodes = []
          data.nodes.forEach((value, index, array) => {
            let node = this.genNode(value.id, value.name, value.description,
              value.create_date, value.color, value.size, value.shape, value.pic)
            nodes.push(node)
          })
          let links = []
          data.relations.forEach((value, index, array) => {
            let link = {
              sid: value.sid,
              tid: value.tid,
              source: value.source,
              target: value.target,
              value: value.value
            }
            links.push(link)
          })
          this.updateGraph(nodes, links)
        })
      }
    }
  },
  methods: {
    clickNode (params) {
      let data = params.data
      let size = ''
      if (data.symbolSize[0] === 35) {
        size = 'S'
      } else if (data.symbolSize[0] === 45) {
        size = 'M'
      } else if (data.symbolSize[0] === 65) {
        size = 'L'
      }
      let info = ''
      let source = ''
      let sourceId = 0
      let graph = this.$refs.graph
      let links = graph.options.series[0].links
      links.forEach((value, index, array) => {
        if (value.tid === data.nid) {
          info = value.value
          source = value.source
          sourceId = value.sid
        }
      })
      let color = '#c23531'
      if (data.itemStyle) {
        color = data.itemStyle.color
      }
      this.$store.commit('setNode', {
        id: data.nid,
        name: data.name,
        desc: data.desc,
        color: color,
        size: size,
        shape: data.symbol,
        info: info,
        pic: data.pic,
        source: source,
        source_id: sourceId,
        create_date: data.create_date
      })
      this.$root.eventHub.$emit('openRightDrawer')
    },
    updateGraph (nodes, links) {
      let graph = this.$refs.graph
      let options = graph.options
      options.series[0].data = nodes
      options.series[0].links = links
      graph.mergeOptions(options)
    },
    addNode (data) {
      let node = this.genNode(data.nid, data.name, data.desc, '',
        data.color, data.size, data.shape)
      let graph = this.$refs.graph
      let options = graph.options
      options.series[0].data.push(node)
      graph.mergeOptions(options)
    },
    updateNode (data) {
      let node = this.genNode(data.nid, data.name, data.desc, '',
        data.color, data.size, data.shape)
      let graph = this.$refs.graph
      let options = graph.options
      let nodes = options.series[0].data
      for (let i = 0; i < nodes.length; i++) {
        if (nodes[i].nid === data.nid) {
          nodes[i] = node
          break
        }
      }
      let links = options.series[0].links
      if (data.value) {
        for (let i = 0; i < links.length; i++) {
          if (links[i].sid === this.node.source_id && links[i].value !== data.value) {
            links[i].value = data.value
            break
          }
        }
      }
      graph.mergeOptions(options)
    },
    delNode (nodeId) {
      let graph = this.$refs.graph
      let options = graph.options
      let data = options.series[0].data
      data.forEach((value, index, array) => {
        if (value.nid === nodeId) {
          array.splice(index, 1)
          graph.mergeOptions(options)
        }
      })
    },
    addLink (data) {
      let graph = this.$refs.graph
      let options = graph.options
      options.series[0].links.push(data)
      graph.mergeOptions(options)
    },
    genNode (nid, name, desc, createDate, color, size, shape, pic) {
      let node = {
        name: name,
        nid: nid,
        desc: desc,
        pic: pic,
        create_date: createDate
      }
      if (color) {
        node['itemStyle'] = { 'color': color }
      }
      if (size === 'L') {
        node['symbolSize'] = [65, 65]
      } else if (size === 'M') {
        node['symbolSize'] = [45, 45]
      } else if (size === 'S') {
        node['symbolSize'] = [35, 35]
      }
      if (shape) {
        node['symbol'] = shape
      }
      return node
    }
  }
}
</script>
