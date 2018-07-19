<template>
  <main >
    <v-toolbar color='indigo'>
      <v-toolbar-title>{{userName}}</v-toolbar-title>
      <add-graph @addGraph="addGraph" />
    </v-toolbar>
    <section>
      <v-list class="mt-3" two-line color='indigo'>
        <v-divider></v-divider>
        <template v-for="item in fashionList">
          <v-list-tile ripple :key="item.id" @click="clickGraph(item)">
            <v-list-tile-action>
              <v-icon>fas fa-fire</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-html="item.name"></v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <del-graph v-bind:graph="item" />
            </v-list-tile-action>
          </v-list-tile>
          <v-divider :key="item.name"></v-divider>
        </template>
        <template v-for="item in graphList">
          <v-list-tile ripple :key="item.id" @click="clickGraph(item)">
            <v-list-tile-action>
              <v-icon>fab fa-cloudsmith</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title v-html="item.name"></v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <del-graph v-bind:graph="item" />
            </v-list-tile-action>
          </v-list-tile>
          <v-divider :key="item.name"></v-divider>
        </template>
      </v-list>
    </section>
  </main>
</template>

<script>
import { mapState } from "vuex";
import AddGraph from "@/views/AddGraph";
import DelGraph from "@/views/DelGraph";

import {
  getFashionGraphs,
  getGraphList,
  updateGraphApi,
  deleteGraphApi
} from "@/api/graph";

export default {
  name: "graph-list",
  components: {
    AddGraph,
    DelGraph
  },
  data() {
    return {
      fashionList: [],
      graphList: []
    };
  },
  computed: {
    ...mapState({
      userId: state => state.user.id,
      userName: state => state.user.name,
      name: state => state.graph.name,
      gid: state => state.graph.id
    })
  },
  created() {
    getFashionGraphs().then(response => {
      this.fashionList = response.data;
      if (this.fashionList.length > 0) {
        this.selectedGraph = this.fashionList[0];
        this.$store.commit("setGraph", this.fashionList[0]);
        // this.$store.dispatch("getNodesByGraph", {
        //   gid: this.fashionList[0].id
        // });
      }
    });
    if (this.userId) {
      getGraphList(this.userId).then(response => {
        this.graphList = response.data;
      });
    }
  },
  methods: {
    clickGraph(graph) {
      this.selectedGraph = graph;
      this.$store.commit("setGraph", { graph });
      this.$store.dispatch("getNodesByGraph", { gid: graph.id });
    },
    addGraph(graph) {
      this.graphList.push(graph);
    }
  }
};
</script>
<style scoped>
.content {
  padding-top: 30px !important;
}
</style>
