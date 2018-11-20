<template>
  <v-card id="create" hover>
    <v-container fluid>
      <img :src="image" height="200px" width="100%" :onerror="defaultImage">
      <v-card-title primary-title>
        <div>
          <div class="headline">{{name}}</div>
          <span class="grey--text">{{desc}}</span>
        </div>
      </v-card-title>
      <v-spacer></v-spacer>
      <v-card-actions>
        <v-btn flat color="purple">更多</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-container>
    <v-speed-dial v-model="fab" :top="false" :bottom="true" :right="true" :left="false" :open-on-hover="true" transition="slide-x-reverse-transition">
      <v-btn slot="activator" v-model="fab" color="blue darken-2" dark fab>
        <v-icon>account_circle</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
      <v-btn fab dark small color="red" @click="delNodeDialog = true">
        <v-icon>delete</v-icon>
      </v-btn>
          <v-btn fab dark small color="indigo" @click="updateNode">
        <v-icon>edit</v-icon>
      </v-btn>
      <v-btn fab dark small color="green" @click="addNode">
        <v-icon>add</v-icon>
      </v-btn>
    </v-speed-dial>
    <v-dialog v-model="delNodeDialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">删除节点: {{name}}</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="delNode">确认</v-btn>
          <v-btn color="green darken-1" flat @click="delNodeDialog = false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-card>
</template>
<style scoped>
/* This is for documentation purposes and will not be needed in your application */

#create {
  height: 100%;
}
#create .v-speed-dial {
  position: absolute;
}
#create .v-btn--floating {
  position: relative;
}
</style>

<script>
import { mapState } from "vuex";
import { delNodeApi } from "@/api/graph";
export default {
  name: "app-right",
  data() {
    return {
      fab: false,
      defaultImage: 'this.src="' + require("../assets/logo.png") + '"',
      delNodeDialog: false,
    };
  },
  computed: {
    activeFab() {
      console.log(this.tabs)
      switch (this.tabs) {
        case "one":
          return { class: "purple", icon: "account_circle" };
        case "two":
          return { class: "red", icon: "edit" };
        case "three":
          return { class: "green", icon: "keyboard_arrow_up" };
        default:
          return {};
      }
    },
    ...mapState({
      nodeId: state => state.node.id,
      name: state => state.node.name,
      desc: state => state.node.desc,
      image: state => {
        if (state.node.pic) {
          return BASE_URL + "/node_pics/" + state.node.pic;
        }
        return require("../assets/logo.png");
      },
      create_date: state => state.node.create_date
    })
  },
  methods: {
    addNode() {
      this.$root.eventHub.$emit("addNodeEvent", true);
    },
    delNode () {
      delNodeApi(this.nodeId).then(response => {
        this.delNodeDialog = false
        this.$root.eventHub.$emit("delNode", this.nodeId);
      })
    },
    updateNode() {
      this.$root.eventHub.$emit("updateNodeEvent")
    }
  }
};
</script>
