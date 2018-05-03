<template>
  <el-form label-width="80px" :label-position='"left"'>
  <el-form-item label="图谱">
    <el-input v-model="graph.name" disabled></el-input>
  </el-form-item>
  <el-form-item label="相关节点">
    <el-input v-model="node" disabled></el-input>
  </el-form-item>
  <el-form-item label="名称">
    <el-input v-model="name"></el-input>
  </el-form-item>
  <el-form-item label="关系">
    <el-input v-model="info"></el-input>
  </el-form-item>
  <el-form-item label="颜色">
    <el-color-picker v-model="color"></el-color-picker>
  </el-form-item>
  <el-form-item label="描述">
    <el-input type="textarea" v-model="desc"></el-input>
  </el-form-item>
  <el-form-item>
    <el-button type="primary" @click="onSubmit">立即创建</el-button>
    <el-button @click="cancle">取消</el-button>
  </el-form-item>
</el-form>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'add-node',
  data: function () {
    return {
      name: '',
      desc: '',
      info: '',
      color: ''
    }
  },
  methods: {
    onSubmit () {
      console.log(this.color)
      this.$store.dispatch('addNode', {
        name: this.name,
        desc: this.desc,
        color: this.color,
        graphId: this.$store.state.graph.id
      })
      this.$emit('closeAddNodeDialog')
    },
    cancle () {
      this.$emit('closeAddNodeDialog')
    }
  },
  computed: mapState({
    node: state => state.node.name,
    user: state => state.user.name,
    graph: state => state.graph
  })
}
</script>
