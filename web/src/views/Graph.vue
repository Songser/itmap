<template>
  <v-graph :width="graph.width" :height="graph.width" :fit-view="graph.fitView" :fit-view-padding="graph.fitViewPadding" :animate="graph.animate" :type="graph.type" :data="data" :on-click="graph.onClick">
    <v-zoom :max="zoom.max" :min="zoom.min"></v-zoom>
  </v-graph>
</template>
<script>
import { mapState } from "vuex";
import { addNodeApi, addLinkApi, getNodesApi, delNodeApi } from "@/api/graph";

const data = {
  nodes: [
    {
      id: "node1",
      x: 100,
      y: 200
    },
    {
      id: "node2",
      x: 300,
      y: 200
    }
  ],
  edges: [
    {
      id: "edge1",
      target: "node2",
      source: "node1"
    }
  ]
};
const graph = {
  type: 'graph',
  width: 500,
  height: 500,
  fitView: 'cc',
  fitViewPadding: true,
  animate: true,
  data
};
const zoom = {
  min: 1,
  max: 10
};
export default {
  name: "graph",
  data() {
    return {
      graph,
      data,
      zoom
    };
  },
  created() {
    this.$root.eventHub.$on("addNode", target => {
      console.log("addNode");
    });
  },
  computed: {
    ...mapState({
      graphId: state => state.graph.id
    })
  },
  watch: {
    graphId(value) {
      if (value) {
        console.log(value);
        getNodesApi(value).then(response => {
          const data = response.data;
          console.log(data);
          let nodes = [];
          data.nodes.forEach((value, index, array) => {
            let node = {
              id: value.id,
              color: value.color,
              shape: value.shape,
              label: value.name,
              desc: value.description,
              create_date: value.create_date,
              index: 1
            };
            if (value.size === "L") {
              node["size"] = [65, 65];
            } else if (value.size === "M") {
              node["size"] = [45, 45];
            } else if (value.size === "S") {
              node["size"] = [35, 35];
            }
            nodes.push(node);
          });
          let edges = [];
          data.relations.forEach((value, index, array) => {
            let edge = {
              target: value.tid,
              source: value.sid,
            };
            edges.push(edge);
          });
          console.log(nodes);
          console.log(edges)
          let nodes2 = [
                {
                  id: "node3",
                },
                {
                  id: "node4",
                },
                {
                  id: "node5",
                },
              ]
            console.log(nodes2)
          this.data = Object.assign(
            {},
            {
              nodes: nodes,
              edges: edges
            }
          );
          this.zoom = Object.assign(
            {},
            {
              min: 1,
              max: 10,
              current: 1
            }
          );
        });
      }
    }
  }
};
</script>
