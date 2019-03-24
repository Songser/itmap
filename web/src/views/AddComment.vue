<template>
  <v-card>
    <v-card-title>
      <p class="title">添加留言</p>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field v-model="title" label="标题" autofocus></v-text-field>
        <v-textarea v-model="desc" label="留言" multi-line rows="5"></v-textarea>
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
  addCommentApi
} from '@/api/comment'

export default {
  name: 'add-comment',
  data () {
    return {
      title: '',
      desc: ''
    }
  },
  computed: {
    ...mapState({
      node: state => state.node,
      user: state => state.user
    })
  },
  methods: {
    init () {
      this.title = ''
      this.desc = ''
    },
    onSubmit () {
      let data = {
        title: this.title,
        description: this.desc,
        owner_name: this.user.name
      }
      addCommentApi(this.node.id, data).then(response => {
        this.$root.eventHub.$emit('addCommentEvent', data)
        this.$emit('closeAddCommentDialog')
        this.init()
      })
    },
    cancle () {
      this.$emit('closeAddCommentDialog')
      this.init()
    }
  }
}
</script>
