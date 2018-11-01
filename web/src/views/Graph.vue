<template>
  <div class="main-graph">
    <chart ref="graph" :options="graph" @click="clickNode"/>
  </div>
</template>

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
      nodes: [],
      links: [],
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
            data: this.nodes,
            links: this.links,
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
          this.nodes = []
          data.nodes.forEach((value, index, array) => {
            let node = {
              id: value.id,
              color: value.color,
              shape: value.shape,
              label: value.name,
              desc: value.description,
              create_date: value.create_date,
              index: 1,
            }
            if (value.size === 'L') {
              node['size'] = [65, 65]
            } else if (value.size === 'M') {
              node['size'] = [45, 45]
            } else if (value.size === 'S') {
              node['size'] = [35, 35]
            }
            this.nodes.push(node)
          })
        })
      }
    }
  },
  methods: {
    clickNode (params) {

    }
  }
}
</script>
