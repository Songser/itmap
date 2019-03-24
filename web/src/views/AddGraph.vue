<template>
  <main>
    <v-btn color="pink" dark small absolute bottom right fab @click="openDialog">
      <v-icon>add</v-icon>
    </v-btn>
    <v-dialog v-model="showDialog" max-width="500px">
      <v-card>
        <v-card-title>
          添加图谱
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="name" name="name" label="名称" type="text"></v-text-field>
          <v-switch v-model="isPrivate" label="私有" color="red" hide-details></v-switch>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" flat @click.stop="addGraph">确定</v-btn>
          <v-btn color="primary" flat @click.stop="showDialog=false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </main>
</template>
<script>
import { mapState } from 'vuex'
import {
  addGraphApi
} from '@/api/graph'

export default {
  name: 'add-graph',
  data () {
    return {
      showDialog: false,
      name: '',
      isPrivate: false
    }
  },
  computed: {
    ...mapState({
      userId: state => state.user.id
    })
  },
  methods: {
    openDialog () {
      if (this.userId) {
        this.showDialog = true
      } else {
        this.$root.eventHub.$emit('snackbar', '请先登录')
      }
    },
    addGraph () {
      addGraphApi(this.userId, this.name, this.isPrivate).then(response => {
        this.$emit('addGraph', { id: response.data, name: this.name })
        this.name = ''
        this.showDialog = false
      })
    }
  }
}
</script>
