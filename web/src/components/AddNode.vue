<template>
  <el-form label-width="80px" :label-position='"left"' :model="graph">
  <el-form-item label="名称">
    <el-input v-model="graph.name"></el-input>
  </el-form-item>
  <el-form-item label="创建人">
    <el-input v-model="graph.user"></el-input>
  </el-form-item>
  <el-form-item label="相关节点">
    <el-input v-model="graph.node"></el-input>
  </el-form-item>
  <el-form-item label="关系名">
    <el-input v-model="graph.relName"></el-input>
  </el-form-item>
  <el-form-item label="描述">
    <el-input v-model="graph.desc"></el-input>
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
      graph: {
        name: '',
        user: '',
        desc: '',
        node: '',
        relName: ''
      }
    }
  },
  methods: {
    onSubmit () {
      this.$store.commit('addNode', this.graph)
      this.$emit('closeAddNodeDialog')
    },
    cancle () {
      this.$emit('closeAddNodeDialog')
    }
  },
  computed: mapState({
    node: state => state.node
  })
}
</script>
