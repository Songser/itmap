<template>
    <v-card>
      <v-list two-line>
      <template v-for="(item, index) in items">
        <v-list-tile :key="item.title" avatar ripple >
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            <v-list-tile-sub-title class="text--primary">{{ item.author }}</v-list-tile-sub-title>
            <v-list-tile-sub-title>{{ item.description }}</v-list-tile-sub-title>
          </v-list-tile-content>

          <v-list-tile-action>

          </v-list-tile-action>
        </v-list-tile>
        <v-divider v-if="index + 1 < items.length" :key="index"></v-divider>
      </template>
    </v-list>
    </v-card>
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
          this.items = response.data
        });
      }
    }),
    this.$root.eventHub.$on('addArticleEvent', (data) => {
      console.log(data)
      items.append(data)
    })
  },
  methods: {

  }
};
</script>
