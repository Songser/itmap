<template>
  <v-container fluid fill-height>
    <v-layout v-scroll:#scroll-target="onScroll" column align-center >
    <v-card hover>
      <v-list three-line subheader>
        <template v-for="(item, index) in items">
          <v-list-tile :key="item.title" avatar ripple :href="item.url" target="_blank">
            <v-list-tile-content>
              <v-list-tile-title>{{item.title}}</v-list-tile-title>
              <!-- <v-list-tile-sub-title class="text--primary">{{ item.author }}</v-list-tile-sub-title> -->
              <v-list-tile-sub-title style="height: 50px;">{{item.description}}</v-list-tile-sub-title>
            </v-list-tile-content>

            <v-list-tile-action>
              <v-list-tile-action-text>{{ item.author }}</v-list-tile-action-text>
            </v-list-tile-action>
          </v-list-tile>
          <v-divider :key="index"></v-divider>
        </template>
      </v-list>
      <v-card-actions v-show="items.length > 0">
        <v-spacer></v-spacer>
        <v-btn flat color="orange" @click="prePage">上一页</v-btn>
        <v-btn flat color="orange" @click="nextPage">下一页</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
    </v-layout>
  </v-container>
</template>
<script>
import { mapState } from "vuex";
import { getArticlesApi } from "@/api/article";
export default {
  name: "app-article",
  data() {
    return {
      nodeId: 0,
      items: [],
      page: 0,
      offsetTop: 0
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
        this.getArticle();
      }
    })
    this.$root.eventHub.$on("addArticleEvent", data => {
      console.log(data);
      this.items.append(data);
    })
  },
  methods: {
    getArticle() {
      getArticlesApi(this.node.id, this.page).then(response => {
        this.nodeId = this.node.id;
        let items = response.data;
        if (items.length > 0) {
          this.items = response.data;
          this.page += 1;
        }
      });
    },
    prePage() {
      this.getArticle();
    },
    nextPage() {
      if (this.page <= 0) {
        return;
      }
      this.page -= 1;
      this.getArticle();
    },
    onScroll (e) {
        this.offsetTop = e.target.scrollTop
      }
  }
};
</script>
