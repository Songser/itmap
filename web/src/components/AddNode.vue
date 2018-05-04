<template>
  <el-form label-width="80px" :label-position='"left"'>
  <el-form-item label="图谱">
    <el-input v-model="graph.name" disabled></el-input>
  </el-form-item>
  <el-form-item label="相关节点">
    <el-input v-model="node.name" disabled></el-input>
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
  <el-form-item label="大小">
    <el-radio v-model="size" label="S">小</el-radio>
    <el-radio v-model="size" label="M">中</el-radio>
    <el-radio v-model="size" label="L">大</el-radio>
  </el-form-item>
  <el-form-item label="形状">
    <el-radio v-model="shape" label="circle">圆形</el-radio>
    <el-radio v-model="shape" label="roundRect">矩形</el-radio>
    <el-radio v-model="shape" label="triangle">三角形</el-radio>
    <el-radio v-model="shape" label="diamond">棱形</el-radio>
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
      color: '#c23531',
      size: 'M',
      shape: 'circle'
    }
  },
  methods: {
    onSubmit () {
      this.$store.dispatch('addNode', {
        graphId: this.graph.id,
        name: this.name,
        color: this.color,
        shape: this.shape,
        size: this.size,
        source_id: this.node.id,
        source: this.node.name,
        target: this.name,
        value: this.info
      })
      this.$emit('closeAddNodeDialog')
    },
    cancle () {
      this.$emit('closeAddNodeDialog')
    }
  },
  computed: mapState({
    node: state => state.node,
    user: state => state.user,
    graph: state => state.graph
  })
}
</script>
