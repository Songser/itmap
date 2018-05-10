<template>
  <el-form label-width="80px" :label-position='"left"'>
  <el-form-item label="图标">
    <el-upload
    name="node_pic"
    :action="action"
  list-type="picture-card"
  :on-preview="handlePictureCardPreview"
  :on-remove="handleRemove"
  :auto-upload="false"
  :http-request="handlerUpload"
  ref="upload">
  <i class="el-icon-plus"></i>
</el-upload>
<el-dialog :visible.sync="dialogVisible">
  <img width="100%" :src="dialogImageUrl" alt="">
</el-dialog>
  </el-form-item>
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
import { getToken } from '@/utils/auth'
import {
  addNodeApi,
  addLinkApi,
  getNodesApi,
  delNodeApi,
  uploadNodePicApi,
} from '@/api/graph'

export default {
  name: 'add-node',
  data: function () {
    return {
      name: '',
      desc: '',
      info: '',
      color: '#c23531',
      size: 'M',
      shape: 'circle',
      dialogImageUrl: '',
      dialogVisible: false,
      action: '',
      newNodeId: 0,
    }
  },
  methods: {
    onSubmit () {
      let data = {
        graphId: this.graph.id,
        name: this.name,
        color: this.color,
        shape: this.shape,
        size: this.size,
        desc: this.desc,
        
      }
      addNodeApi(data).then(response => {
        this.newNodeId = response.data
        data['target_id'] = this.newNodeId
        this.$store.commit('addNode', data)
        this.$refs.upload.submit()
        if (this.node.name && this.name){
          addLinkApi({
            source_id: this.node.id,
            target_id: this.newNodeId,
            graphId:  this.graph.id,
            value: this.info
          }).then(response => {
            this.$store.commit('addLink', {
            source: this.node.name,
            target: this.name,
            value: this.info,
          })
          })
        }
      })
      
      this.$emit('closeAddNodeDialog')
    },
    cancle () {
      this.$emit('closeAddNodeDialog')
    },
    handleRemove(file, fileList) {
      
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handlerUpload(options){
      console.log(options)
      let form = new FormData()
      form.append(options.filename, options.file)
      uploadNodePicApi(form, this.newNodeId)
    }
  },
  computed: mapState({
    node: state => state.node,
    user: state => state.user,
    graph: state => state.graph,
  })
}
</script>
