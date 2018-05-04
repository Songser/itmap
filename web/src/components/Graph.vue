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
  margin: 0px;
  padding: 0px;
}
</style>

<script>
import { mapState } from 'vuex'
import ECharts from 'vue-echarts/components/ECharts'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/graph'
import 'echarts/lib/component/tooltip'

export default {
  components: {
    chart: ECharts
  },
  computed: {
    ...mapState({
      nodes: state => state.node.nodes,
      links: state => state.node.links
    })
  },
  created () {

  },
  watch: {
    nodes (value) {
      let graph = this.$refs.graph
      let options = graph.options
      options.series[0].data = this.nodes
      options.series[0].links = this.links
      graph.mergeOptions(options)
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
  },
  data: function () {
    return {
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
            data: this.$store.state.node.nodes,
            links: this.$store.state.node.links,
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
  }
}
</script>
