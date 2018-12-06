<template>
  <v-card>
    <v-toolbar card dark tabs color="primary">
      <v-btn icon dark @click="closeDialog" >
        <v-icon >close</v-icon>
      </v-btn>
      <!-- <v-toolbar-title>{{node.name}}</v-toolbar-title> -->

      <v-tabs color="primary" v-model="tabs" slider-color="yellow" centered fixed-tabs>
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
      <v-btn icon dark @click="closeDialog" >
        <v-icon >close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card-text style="height:100%">
    <v-layout row >
      <v-flex xs12 sm3>
      </v-flex>
      <v-flex xs12 sm6>
        <v-tabs-items fill-height>
          <v-tab-item value="article" fill-height>
            <app-article fill-height></app-article>
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
      </v-flex>
    </v-layout>
    </v-card-text>
    <v-fab-transition mb-3 mr-3>
      <v-btn :color="activeFab.color" :key="activeFab.icon" v-model="fab" dark fab bottom left @click="add">
        <v-icon>{{ activeFab.icon }}</v-icon>
        <v-icon>close</v-icon>
      </v-btn>
    </v-fab-transition>
    <v-dialog v-model="addArticleDialog" max-width="600px" persistent>
        <add-article @closeAddArticleDialog="closeAddArticleDialog" @openAddArticleDialog="openAddArticleDialog" />
      </v-dialog>
  </v-card>
</template>
<script>
import AppArticle from "@/views/Article";
import AddArticle from "@/views/AddArticle"
import { mapState } from "vuex";
export default {
  name: "node-info",
  components: {
    AppArticle,
    AddArticle
  },
  data() {
    return {
      model: '',
      tabs: "article",
      fab: false,
      addArticleDialog: false,
    };
  },
  created() {
    this.$root.eventHub.$on("showDetailDialog", target => {
      this.$root.eventHub.$emit("showArticleEvent");
      this.openDialog();
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
    add () {
      if (this.tabs == 'article') {
        this.addArticleDialog = true
      }
    },
    showArticle () {
      this.$root.eventHub.$emit('showArticleEvent')
    },
    closeDialog() {
      this.$emit("closeDetailDialog");
    },
    openDialog() {
      this.model = "article";
      this.$emit("openDetailDialog");
    },
    closeAddArticleDialog(data) {
      this.addArticleDialog = false
    },
    openAddArticleDialog () {

    }
  }
};
</script>
<style>
.closebtn {
  position: fixed;
  left: 30px;
  top: 10px;
  z-index: 300;
}
</style>
