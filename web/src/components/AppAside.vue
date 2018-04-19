<template>
  <div>
    <el-input v-model="nodeName" placeholder="请输入内容"></el-input>
    <el-button type="primary" @click="addNode">添加</el-button>
    <div>{{node.name}}</div>
  </div>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'app-aside',
  data: function () {
    return {
      nodeName: ''
    }
  },
  methods: {
    addNode () {
      this.$store.commit('addNode', this.nodeName)
    }
  },
  computed: mapState({
    node: state => state.node
  })
}
</script>
