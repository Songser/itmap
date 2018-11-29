<template>
  <v-card tile>
    <v-toolbar card dark tabs color="primary">
      <v-btn icon dark @click="closeDialog">
        <v-icon>close</v-icon>
      </v-btn>
      <v-toolbar-title>{{node.name}}</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tabs color="primary" v-model="model" slider-color="yellow" fixed-tabs >
        <v-tab href="#article" @click="showArticle">
          文章
        </v-tab>
        <v-tab href="#comment">
          留言
        </v-tab>
        <v-tab href="#user">
          用户
        </v-tab>
        <v-tab href="#book">
          书籍
        </v-tab>
      </v-tabs>
      <v-btn icon>
        <v-icon>add</v-icon>
      </v-btn>
    </v-toolbar>
    <v-tabs-items v-model="model">
      <v-tab-item value="article">
        <app-article></app-article>
      </v-tab-item>
      <v-tab-item value="comment">
        comment
      </v-tab-item>
      <v-tab-item value="user">
        user
      </v-tab-item>
      <v-tab-item value="book">
        book
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>
<script>
import AppArticle from '@/views/Article'
import { mapState } from "vuex";
export default {
  name: "node-info",
  components: {
    AppArticle,
  },
  data () {
    return {
      model: 'article',
    }
  },
  created () {
    this.$root.eventHub.$on('showDetailDialog',(target) => {
      this.$root.eventHub.$emit('showArticleEvent')
      this.openDialog()
    });
  },
  computed: {
    ...mapState({
      node: state => state.node
    })
  },
  methods: {
    closeDialog() {
      this.$emit("closeDetailDialog");
    },
    openDialog() {
      this.model = 'article'
      this.$emit("openDetailDialog");
    },
    showArticle() {
      console.log('fff')
    }
  }
};
</script>
<style>
.v-toolbar .v-tabs {
  width: 80%;
}
</style>
