<template>
  <v-card>
    <v-card-title>
      <p class="title">添加文章</p>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field v-model="title" label="标题" autofocus></v-text-field>
        <v-text-field v-model="url" label="链接"></v-text-field>
        <v-text-field v-model="author" label="作者"></v-text-field>
        <v-text-field v-model="source" label="来源"></v-text-field>
        <v-textarea v-model="desc" label="描述" multi-line rows="3"></v-textarea>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="onSubmit">确定</v-btn>
      <v-btn color="primary" @click="cancle">取消</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import {
  addArticleApi
} from '@/api/article'

export default {
  name: 'add-article',
  data () {
    return {
      title: '',
      url: '',
      author: '',
      source: '',
      desc: ''
    }
  },
  computed: {
    ...mapState({
      node: state => state.node
    })
  },
  methods: {
    init () {
      this.title = '',
      this.url = '',
      this.author = '',
      this.source = '',
      this.desc = ''
    },
    onSubmit () {
      let data = {
        title: this.title,
        url: this.url,
        author: this.author,
        source: this.source,
        description: this.desc
      }
      addArticleApi(this.node.id, data).then(response => {
        this.$root.eventHub.$emit('addArticleEvent', data)
        this.$emit('closeAddArticleDialog')
        this.init()
      })
    },
    cancle () {
      this.$emit('closeAddArticleDialog')
      this.init()
    }
  }
}
</script>
