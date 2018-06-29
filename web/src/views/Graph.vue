<template>
  <section>
    <div id='graph'>

    </div>
  </section>
</template>
<script>
import G6 from '@antv/g6'

export default {
  name: 'graph',
  data () {
    let graph = new G6.Graph({
      container: 'graph',
      width: 600,
      height: 300
    })
    let data = {
      nodes: [
        {
          id: 'node1',
          x: 100,
          y: 200
        },
        {
          id: 'node2',
          x: 300,
          y: 200
        }
      ],
      edges: [
        {
          id: 'edge1',
          target: 'node2',
          source: 'node1'
        }
      ]
    }
    graph.read(data)
    return {
      graph: graph
    }
  }
}
</script>
