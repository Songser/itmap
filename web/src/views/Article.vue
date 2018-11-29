<template>
<v-layout row>
  <v-flex xs12 sm6 offset-sm3>
    <v-card>
      <v-list two-line>
      <template v-for="(item, index) in items">
        <v-list-tile :key="item.title" avatar ripple @click="toggle(index)">
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            <v-list-tile-sub-title class="text--primary">{{ item.headline }}</v-list-tile-sub-title>
            <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action>
            <v-list-tile-action-text>{{ item.action }}</v-list-tile-action-text>
            <v-icon v-if="selected.indexOf(index) < 0" color="grey lighten-1">
              star_border
            </v-icon>

            <v-icon v-else color="yellow darken-2">
              star
            </v-icon>
          </v-list-tile-action>
        </v-list-tile>
        <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
      </template>
    </v-list>
    </v-card>
  </v-flex>
</v-layout>
</template>
<script>
import { mapState } from "vuex";
import { getArticlesApi } from "@/api/article";
export default {
  name: "app-article",
  data() {
    return {
      nodeId: 0,
      items: []
    };
  },
  computed: {
    ...mapState({
      node: state => state.node
    })
  },
  created() {
    this.$root.eventHub.$on("showArticleEvent", () => {
      if (this.nodeId != this.node.id) {
        getArticlesApi(this.node.id).then(response => {
          this.nodeId = this.node.id
          console.log(response);
        });
      }
    })
  },
  methods: {

  }
};
</script>
