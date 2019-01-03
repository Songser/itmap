<template>
  <v-card>
    <v-container
      fluid
      grid-list-lg
      mx-0
    >
      <!-- <v-list three-line subheader> -->
      <v-layout
        row
        wrap
      >
        <template v-for="(item, index) in items">
          <v-flex
            xs12
            :key="item.id"
          >
            <v-card
              hover
              color="blue-grey darken-1"
              class="white--text elevation-6"
              @mouseenter="selectStyle(index)"
              @mouseleave="outStyle(index)"
            >
              <v-card-title primary-title>
                <div>
                  <div class="headline">{{item.title}}</div>
                  <div>{{item.description}}</div>
                </div>
              </v-card-title>
              <v-divider light></v-divider>
              <v-card-actions class="pa-3">
                <span
                  class="grey--text"
                  style="margin-right:5px"
                >作者: </span> {{item.author}}
                <v-spacer></v-spacer>
                <v-icon
                  @click="editArticle(item)"
                  v-show="active == index && user.id == item.owner_id">
                  edit
                </v-icon>
                <v-icon
                  v-show="active == index && user.id == item.owner_id">delete</v-icon>
                <v-icon>star_border</v-icon>
              </v-card-actions>
            </v-card>
          </v-flex>
        </template>
      </v-layout>
      <!-- </v-list> -->
      <v-card-actions v-show="items.length > 0">
        <v-btn
          flat
          color="orange"
          @click="prePage"
        >上一页</v-btn>
        <v-spacer></v-spacer>
        <v-btn
          flat
          color="orange"
          @click="nextPage"
        >下一页</v-btn>
      </v-card-actions>
    </v-container>
    <v-dialog
      v-model="showDialog"
      max-width="600px"
      persistent
    >
      <add-article @closeAddArticleDialog="closeAddArticleDialog" />
    </v-dialog>
  </v-card>
</template>
<script>
import { mapState } from "vuex";
import { getArticlesApi } from "@/api/article";
import AddArticle from "@/views/AddArticle";
export default {
  name: "app-article",
  components: {
    AddArticle
  },
  props: ["addArticle"],
  data() {
    return {
      nodeId: 0,
      items: [],
      page: 0,
      offsetTop: 0,
      active: -1,
      showDialogModel: false
    };
  },
  computed: {
    ...mapState({
      node: state => state.node,
      user: state => state.user
    }),
    showDialog() {
      return this.addArticle;
    }
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
      getArticlesApi(this.node.id, this.page).then(response => {
        this.nodeId = this.node.id;
        let items = response.data;
        console.log(items);
        if (items.length > 0) {
          this.items = items;
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
      if (this.items.length < 20) {
        return;
      }
      this.page += 1;
      this.getArticle();
    },
    onScroll(e) {
      this.offsetTop = e.target.scrollTop;
    },
    selectStyle(index) {
      this.active = index;
    },
    outStyle(index) {
      this.active = -1;
    },
    closeAddArticleDialog(data) {
      this.$emit("closeDialog");
    },
    editArticle(item){

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
