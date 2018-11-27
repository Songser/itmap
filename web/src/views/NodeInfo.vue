<template>
  <v-card tile>
    <v-toolbar card dark color="primary">
      <v-btn icon dark @click="closeDialog">
        <v-icon>close</v-icon>
      </v-btn>
      <!-- <v-toolbar-title>Settings</v-toolbar-title> -->
      <v-spacer></v-spacer>
      <v-tabs color="primary" v-model="model" slider-color="yellow" fixed-tabs >
        <v-tab href="#article">
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

    </v-toolbar>
    <v-tabs-items v-model="model">
      <v-tab-item value="article">
        ddddd
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
  methods: {
    closeDialog() {
      this.$emit("closeDetailDialog");
    }
  }
};
</script>
