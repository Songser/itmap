<template>
  <div class="main-graph">
    <chart :options="graph" @click="clickNode"/>
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
import ECharts from 'vue-echarts/components/ECharts'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/graph'
import 'echarts/lib/component/tooltip'

export default {
  components: {
    chart: ECharts
  },
  methods: {
    addNode () {
      let graph = this.graph
      let data = graph.series[0].data
      data.push({
        name: '呵呵',
        draggable: true
      })
      let link = graph.series[0].links
      link.push({
        source: '徐贱云',
        target: '呵呵',
        value: '朋友'
      })
    },
    clickNode (params) {
      this.$store.commit('setNode', params)
    }
  },
  created () {
    this.$store.dispatch('getGraph')
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
            categories: [{
              name: '朋友',
              itemStyle: {
                normal: {
                  color: '#009800'
                }
              }
            }, {
              name: '战友',
              itemStyle: {
                normal: {
                  color: '#4592ff'
                }
              }
            }, {
              name: '亲戚',
              itemStyle: {
                normal: {
                  color: '#3592ff'
                }
              }
            }],
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
