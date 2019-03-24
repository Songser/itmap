<template>
  <div>
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
              color="light-blue lighten-2"
              class="white--text elevation-6"
              @mouseenter="selectStyle(index)"
              @mouseleave="outStyle(index)"
            >
              <v-layout row>
                <v-flex xs8>
                  <v-card-title primary-title>
                    <div>
                      <div class="headline black--text">{{item.name}}</div>
                      <div class="black--text">{{item.description}}</div>
                    </div>
                  </v-card-title>
                </v-flex>
                <v-flex xs4>
                  <img
                    :src="image + item.pic"
                    alt="trevor"
                    :onerror="defaultImage"
                    height="150px"
                    width="100px"
                  />
                </v-flex>
              </v-layout>
              <v-divider light></v-divider>
              <v-card-actions class="pa-3">
                <span
                  class="grey--text"
                  style="margin-right:5px"
                >作者: </span> <p class="black--text"> {{item.author}}</p>
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
      <v-card-actions v-show="items.length >= 20 && page > 0">
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
      <add-book @closeAddBookDialog="closeAddBookDialog" />
    </v-dialog>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import AddBook from '@/views/AddBook'
import { getBooksApi } from '@/api/book'
export default {
  name: 'app-book',
  components: {
    AddBook
  },
  props: ['addBook'],
  data () {
    return {
      nodeId: 0,
      items: [],
      page: 0,
      offsetTop: 0,
      active: -1,
      showDialogModel: false,
      image: process.env.BASE_URL + '/book_pics/',
      defaultImage: 'this.src="' + require('../assets/logo.png') + '"'
    }
  },
  computed: {
    ...mapState({
      node: state => state.node
    }),
    showDialog () {
      return this.addBook
    }
  },
  created () {
    this.$root.eventHub.$on('showBookEvent', () => {
      if (this.nodeId !== this.node.id) {
        this.getBook()
      }
    })
    this.$root.eventHub.$on('addBookEvent', data => {
      this.items.push(data)
    })
  },
  methods: {
    getBook () {
      getBooksApi(this.node.id, this.page).then(response => {
        this.nodeId = this.node.id
        let items = response.data
        if (items.length > 0) {
          this.items = response.data
        }
      })
    },
    prePage () {
      if (this.page <= 0) {
        return
      }
      this.page -= 1
      this.getBook()
    },
    nextPage () {
      if (this.items.length < 20) {
        return
      }
      this.page += 1
      this.getBook()
    },
    onScroll (e) {
      this.offsetTop = e.target.scrollTop
    },
    selectStyle (index) {
      this.active = index
    },
    outStyle (index) {
      this.active = -1
    },
    closeAddBookDialog (data) {
      this.$emit('closeDialog')
    }
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
img {
  margin-top: 30px;
}
</style>
