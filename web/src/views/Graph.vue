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
  width: 80%;
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
import { addNodeApi, addLinkApi, getNodesApi, delNodeApi } from "@/api/graph";


export default {
  name: 'graph',
  components: {
    chart: ECharts
  },
  computed: {
    ...mapState({
      graphId: state => state.graph.id
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
    graphId(value) {
      console.log(this.graphId)
      if (value) {
        if (this.oldGraphId == value){
          return
        }
        this.oldGraphId = value
        getNodesApi(value).then(response => {
          const data = response.data;
          console.log('===', data);
          let nodes = []
          data.nodes.forEach((value, index, array) => {
            let node = {
              name: value.name,
              nid: value.id,
              desc: value.description,
              create_date: value.create_date
            }
            if (value.color) {
              node['itemStyle'] = { 'color': value.color }
            }
            if (value.size === 'L') {
              node['symbolSize'] = [65, 65]
            } else if (value.size === 'M') {
              node['symbolSize'] = [45, 45]
            } else if (value.size === 'S') {
              node['symbolSize'] = [35, 35]
            }
            if (value.shape) {
              node['symbol'] = value.shape
            }
            nodes.push(node)
          })
          let links = []
          data.relations.forEach((value, index, array) => {
            let link = {
              source: value.source,
              target: value.target,
              value: value.value,
            }
            links.push(link)
          })
          let graph = this.$refs.graph
          let options = graph.options
          options.series[0].data = nodes
          options.series[0].links = links
          graph.mergeOptions(options)
          if (nodes.length > 0){
            console.log(nodes)
            this.$store.commit('setNode', {
              id: nodes[0].nid,
              name: nodes[0].name,
              desc: nodes[0].desc,
              create_date: nodes[0].create_date
            })
          }
        })
      }
    }
  },
  methods: {
    clickNode (params) {
      let data = params.data
      this.$store.commit('setNode', {
        id: data.nid,
        name: data.name,
        desc: data.desc,
        create_date: data.create_date
      })
    }
  }
}
</script>
