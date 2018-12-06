<template>
  <v-card>
    <v-container fluid grid-list-lg mx-0>
      <!-- <v-list three-line subheader> -->
      <v-layout row wrap>
        <template v-for="(item) in items">
          <v-flex xs12 :key="item.id">
            <v-card hover color="blue-grey darken-1" class="white--text elevation-6" >
              <v-card-title primary-title>
                <div>
                  <div class="headline">{{item.title}}</div>
                  <div>{{item.description}}</div>
                </div>
              </v-card-title>

              <v-divider light></v-divider>
              <v-card-actions class="pa-3">
                <span class="grey--text" style="margin-right:5px">作者: </span> {{item.author}}
                <v-spacer></v-spacer>
                <v-icon>star_border</v-icon>
                <v-icon>edit</v-icon>
                <v-icon>delete</v-icon>
              </v-card-actions>
            </v-card>
          </v-flex>
        </template>
      </v-layout>
      <!-- </v-list> -->
      <v-card-actions v-show="items.length > 0">
        <v-btn flat color="orange" @click="prePage">上一页</v-btn>
        <v-spacer></v-spacer>
        <v-btn flat color="orange" @click="nextPage">下一页</v-btn>
      </v-card-actions>
    </v-container>
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
    });
    this.$root.eventHub.$on("addArticleEvent", data => {
      this.items.push(data);
    });
  },
  methods: {
    getArticle() {
      console.log(this.page)
      getArticlesApi(this.node.id, this.page).then(response => {
        this.nodeId = this.node.id;
        let items = response.data;
        if (items.length > 0) {
          this.items = response.data;
          console.log(this.page)
        }
      });
    },
    prePage() {
      if (this.page <= 0) {
        return;
      }
      this.page -= 1;
      this.getArticle();
    },
    nextPage() {
      if (this.items.length < 20){
        return
      }
      this.page += 1;
      this.getArticle();
    },
    onScroll(e) {
      this.offsetTop = e.target.scrollTop;
    }
  }
};
</script>
<style scoped>
.v-card {
  box-shadow: none;
}
.container {
  padding: 0px;
}
</style>
