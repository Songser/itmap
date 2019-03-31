<template>
<div>
  <el-card class="box-card-component" style="margin-left:8px;">
    <div slot="header" class="box-card-header">
      <img src='https://wpimg.wallstcn.com/e7d23d71-cf19-4b90-a1cc-f56af8c0903d.png'>
    </div>
    <div style="position:relative;">
      <pan-thumb class="panThumb" :image="image"></pan-thumb>
      <div style="padding-top:35px;" class='progress-item'>
        <h3>节点: {{name}}</h3>
      </div>
      <div class='progress-item'>
        <span>图谱:</span>
        <span>{{graph}}</span>
      </div>
      <div class='progress-item'>
        <span>创建人:</span>
        <span>{{user}}</span>
      </div>
      <div class='progress-item'>
        <span>描述:</span>
        <div>{{desc}}</div>
      </div>
       <div class='progress-item'>
        <span>创建日期:</span>
        <span>{{create_date}}</span>
      </div>
      <div>
        <el-button type="success" icon="el-icon-circle-plus-outline"  circle @click="showAddNodeDialog"></el-button>
        <el-button type="success" icon="el-icon-remove-outline"  circle @click="showDeleteNodeDialog"></el-button>
      </div>
    </div>
  </el-card>
  <el-dialog
    title="添加节点"
    :visible.sync="addNodeDialog"
    width="500px"
    :append-to-body=true>
    <add-node @closeAddNodeDialog="addNodeClose"/>
  </el-dialog>
  <el-dialog
    title="删除节点"
    :visible.sync="delNodeDialog"
    width="500px"
    :append-to-body=true>
    <span>删除节点{{name}}</span>
    <span slot="footer" class="dialog-footer">
    <el-button @click="delNodeDialog = false">取 消</el-button>
    <el-button type="primary" @click="delNodeClose">确 定</el-button>
  </span>
  </el-dialog>
</div>
</template>

<script>
import logo from '@/assets/it.jpg'
import PanThumb from '@/components/PanThumb'
import AddNode from '@/components/AddNode'
import { mapState } from 'vuex'
export default {
  name: 'node-info',
  components: { PanThumb, AddNode },
  data () {
    return {
      statisticsData: {
        article_count: 1024,
        pageviews_count: 1024
      },
      addNodeDialog: false,
      delNodeDialog: false,
      defaultImg: logo
    }
  },
  computed: mapState({
    id: state => state.node.id,
    name: state => state.node.name,
    user: state => state.graph.ownerName,
    desc: state => state.node.desc,
    create_date: state => state.node.create_date,
    graph: state => state.graph.name,
    image: state => process.env.BASE_API + '/node_pics/' + state.node.id + '.jpg'
  }),
  methods: {
    showAddNodeDialog () {
      this.addNodeDialog = true
    },
    addNodeClose () {
      this.addNodeDialog = false
    },
    showDeleteNodeDialog () {
      this.delNodeDialog = true
    },
    delNodeClose () {
      this.delNodeDialog = false
      this.$store.dispatch('delNode', {id: this.id, name: this.name})
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" >
.box-card-component{
  .el-card__header {
    padding: 0px!important;
  }
}
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.box-card-component {
  text-align: left;
  .box-card-header {
    position: relative;
    height: 220px;
    img {
      width: 100%;
      height: 100%;
      transition: all 0.2s linear;
      &:hover {
        transform: scale(1.1, 1.1);
        filter: contrast(130%);
      }
    }
  }
  .mallki-text {
    position: absolute;
    top: 0px;
    right: 0px;
    font-size: 20px;
    font-weight: bold;
  }
  .panThumb {
    z-index: 100;
    height: 70px!important;
    width: 70px!important;
    position: absolute!important;
    top: -45px;
    left: 0px;
    border: 5px solid #ffffff;
    background-color: #fff;
    margin: auto;
    box-shadow: none!important;
    /deep/ .pan-info {
      box-shadow: none!important;
    }
  }
  .progress-item {
    margin-bottom: 10px;
    font-size: 14px;
  }
  @media only screen and (max-width: 1510px){
    .mallki-text{
      display: none;
    }
  }
}
</style>
