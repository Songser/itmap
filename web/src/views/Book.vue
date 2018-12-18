<template>
<v-card>
    <v-container fluid grid-list-lg mx-0>
      <!-- <v-list three-line subheader> -->
      <v-layout row wrap>
        <template v-for="(item, index) in items">
          <v-flex xs12 :key="item.id">
            <v-card hover color="blue-grey darken-1"
              class="white--text elevation-6"
              @mouseenter="selectStyle(index)"
              @mouseleave="outStyle(index)">
              <v-layout row>
                <v-flex xs7>
              <v-card-title primary-title>
                <div>
                  <div class="headline">{{item.title}}</div>
                  <div>{{item.description}}</div>
                </div>
              </v-card-title>
               </v-flex>
               <v-flex xs5>
                 <v-img
                    src="https://cdn.vuetifyjs.com/images/cards/halcyon.png"
                    height="125px"
                    contain
                  ></v-img>
               </v-flex>
               </v-layout>
              <v-divider light></v-divider>
              <v-card-actions class="pa-3">
                <span class="grey--text" style="margin-right:5px">作者: </span> {{item.author}}
                <v-spacer></v-spacer>
                <v-icon v-show="active == index">edit</v-icon>
                <v-icon v-show="active == index">delete</v-icon>
                <v-icon>star_border</v-icon>
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
    <v-dialog
      v-model="showDialog"
      max-width="600px"
      persistent
    >
      <!-- <add-book
        @closeAddBookDialog="closeAddBookDialog"
      /> -->
    </v-dialog>
  </v-card>
</template>
<script>
import { mapState } from "vuex";
// import AddComment from "@/views/AddComment";
import { getBooksApi } from "@/api/book";
export default {
  name: 'app-book',
  props: ['addBook'],
  data() {
    return {
      nodeId: 0,
      items: [],
      page: 0,
      offsetTop: 0,
      active: -1,
      showDialogModel: false,
    };
  },
  computed: {
    ...mapState({
      node: state => state.node
    }),
    showDialog() {
      return this.addBook
    }
  },
  created() {
    this.$root.eventHub.$on("showBookEvent", () => {
      if (this.nodeId != this.node.id) {
        this.getBook();
      }
    });
    this.$root.eventHub.$on("addBookEvent", data => {
      this.items.push(data);
    });
  },
  methods: {
    getBook() {
      getBooksApi(this.node.id, this.page).then(response => {
        this.nodeId = this.node.id;
        let items = response.data;
        if (items.length > 0) {
          this.items = response.data;
        }
      });
    },
    prePage() {
      if (this.page <= 0) {
        return;
      }
      this.page -= 1;
      this.getBook();
    },
    nextPage() {
      if (this.items.length < 20){
        return
      }
      this.page += 1;
      this.getBook();
    },
    onScroll(e) {
      this.offsetTop = e.target.scrollTop;
    },
    selectStyle(index) {
      this.active = index
    },
    outStyle(index) {
      this.active = -1
    },
    closeAddBookDialog(data) {
      this.$emit('closeDialog')
    },
  }
}
</script>
<style scoped>
.v-card {
  box-shadow: none;
}
.container {
  padding: 0px;
}
</style>


