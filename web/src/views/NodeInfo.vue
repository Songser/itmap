<template>
  <v-card>
    <v-toolbar
      card
      dark
      tabs
      color="primary"
    >
      <v-btn
        icon
        dark
        @click="closeDialog"
      >
        <v-icon>close</v-icon>
      </v-btn>
      <!-- <v-toolbar-title>{{node.name}}</v-toolbar-title> -->

      <v-tabs
        color="primary"
        v-model="tabs"
        slider-color="yellow"
        centered
        fixed-tabs
      >
        <v-tab
          href="#article"
        >
          文章
        </v-tab>
        <v-tab href="#comment">
          留言
        </v-tab>
        <v-tab href="#book">
          书籍
        </v-tab>
        <v-tab href="#user">
          用户
        </v-tab>
      </v-tabs>
      <v-btn
        icon
        dark
        @click="closeDialog"
      >
        <v-icon>close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text style="height:100%">
      <v-layout row>
        <v-flex
          xs12
          sm3
        >
        </v-flex>
        <v-flex
          xs12
          sm6
        >
          <v-tabs-items v-model="tabs">
            <v-tab-item
              value="article"
            >
              <app-article :addArticle="addArticle"
                @closeDialog="addArticle=false"></app-article>
            </v-tab-item>
            <v-tab-item value="comment">
              <app-comment :addComment="addComment"
                @closeDialog="addComment=false"></app-comment>
            </v-tab-item>
            <v-tab-item value="book">
              <app-book :addBook="addBook"
                @closeDialog="addBook=false"></app-book>
            </v-tab-item>
            <v-tab-item value="user">
              user
            </v-tab-item>
          </v-tabs-items>
        </v-flex>
      </v-layout>
    </v-card-text>
    <v-fab-transition
      mb-3
      mr-3
    >
      <v-btn
        :color="activeFab.color"
        :key="activeFab.icon"
        v-model="fab"
        dark
        fab
        bottom
        left
        @click="add"
      >
        <v-icon>{{ activeFab.icon }}</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
    </v-fab-transition>
  </v-card>
</template>
<script>
import AppArticle from "@/views/Article";
import AppComment from "@/views/Comment";
import AppBook from "@/views/Book";

import { mapState } from "vuex";
export default {
  name: "node-info",
  components: {
    AppArticle,
    AppComment,
    AppBook,
  },
  data() {
    return {
      model: "",
      tabs: "article",
      fab: false,
      addArticle: false,
      addComment: false,
      addBook: false,
      nodeId: 0,
    };
  },
  created() {
    this.$root.eventHub.$on("showDetailDialog", target => {
      this.openDialog();
      this.init();
    });
  },
  computed: {
    ...mapState({
      node: state => state.node
    }),
    activeFab() {
      switch (this.tabs) {
        case "article":
          return { color: "indigo", icon: "add" };
        case "comment":
          return { color: "red", icon: "chat" };
        case "user":
          return { color: "green", icon: "edit" };
        case "book":
          return { color: "blue", icon: "book" };
        default:
          return {};
      }
    }
  },
  methods: {
    add() {
      switch (this.tabs) {
        case "article":
          this.addArticle = true;
          break;
        case "comment":
          this.addComment = true;
          break;
        case "book":
          this.addBook = true;
          break;
      }
    },
    init() {
      if (this.nodeId == this.node.id){
        return
      }
      this.$root.eventHub.$emit("showArticleEvent");
      this.$root.eventHub.$emit("showCommentEvent");
      this.$root.eventHub.$emit("showBookEvent");
    },
    closeDialog() {
      this.$emit("closeDetailDialog");
    },
    openDialog() {
      this.$emit("openDetailDialog");
    },
  }
};
</script>
