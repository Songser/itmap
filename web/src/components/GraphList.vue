<template>
  <div>
    <div class="buttons">
      <el-button type="primary" icon="el-icon-news" circle @click="showAddGraphDialog"></el-button>
      <el-button type="primary" icon="el-icon-edit" circle @click="editGraph"></el-button>
      <el-button type="primary" icon="el-icon-delete" circle @click="deleteGraph"></el-button>
    </div>
   <el-menu
      mode="vertical"
      :show-timeout="200"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
     <el-menu-item index="'graph.id'" v-for="graph in fashionList" :key="graph.name" >
        <span slot="title">
            <a @click="clickGraph(graph.id, graph.name)">{{graph.name}}</a>
        </span>
      </el-menu-item>
      <el-menu-item :index="'graph.id'" v-for="graph in graphList" :key="graph.id">
        <span slot="title">
            <a @click="clickGraph(graph.id, graph.name)">{{graph.name}}</a>
        </span>
    </el-menu-item>
    </el-menu>
    <el-dialog
    title="添加图谱"
    :visible.sync="dialogVisible"
    width="50%" :append-to-body=true>

  <el-input v-model="newGraphName"></el-input>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addNewGraph">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>
<script>
import http from '@/utils/request'
import { mapState } from 'vuex'

import {
  getFashionGraphs,
  getGraphList,
  addGraph
} from '@/api/graph'

export default {
  name: 'graph-list',
  data () {
    return {
      fashionList: [],
      graphList: [],
      dialogVisible: false,
      newGraphName: ''
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.graph.name
    })
  },
  created () {
    getFashionGraphs().then((response) => {
      this.fashionList = response.data
      if (this.fashionList.length > 0) {
        this.$store.commit('setGraphName', this.fashionList[0].name)
        this.$store.dispatch('getNodesByGraph', {gid: this.fashionList[0].id})
      }
    })
    if (this.user_id) {
      getGraphList(this.user_id).then((response) => {
        this.graphList = response.data
        console.log(this.graphList)
      })
    }
  },
  methods: {
    showAddGraphDialog () {
      this.dialogVisible = true
    },
    addNewGraph () {
      addGraph(this.user_id, this.newGraphName).then((response) => {
        this.graphList.push({id: response.data, name: this.newGraphName})
        this.newGraphName = ''
        this.dialogVisible = false
      })
    },
    editGraph () {

    },
    deleteGraph () {

    },
    clickGraph (gid, name) {
      this.$store.commit('setGraph', {id: gid, name})
      this.$store.dispatch('getNodesByGraph', {gid: gid})
    }
  }
}
</script>

<style scoped>
.buttons {
  margin: 10px;
}
.el-dialog {
    text-align: left;
}
</style>
