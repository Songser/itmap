<template>
  <div>
    <div class="buttons">
      <el-button type="primary" icon="el-icon-news" circle @click="showAddGraphDialog"></el-button>
      <el-button type="primary" icon="el-icon-edit" circle @click="showEditGraphDialog"></el-button>
      <el-button type="primary" icon="el-icon-delete" circle @click="deleteGraph"></el-button>
    </div>
   <el-menu
      mode="vertical"
      :show-timeout="200"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
    <template v-for="graph in fashionList">
     <el-menu-item :index="'graph.name'"  :key="graph.name" >
        <span slot="title">
            <a @click="clickGraph(graph)">{{graph.name}}</a>
        </span>
      </el-menu-item>
    </template>
    <template v-for="graph in graphList">
      <el-menu-item index="'graph.id'"  :key="graph.id">
        <span slot="title">
            <a @click="clickGraph(graph)">{{graph.name}}</a>
        </span>
    </el-menu-item>
    </template>
    </el-menu>
    <el-dialog
    title="添加图谱"
    :visible.sync="dialogVisible"
    width="50%" :append-to-body=true>
  <el-input v-model="newGraphName"></el-input>
  <el-switch
  v-model="isPrivate"
  active-color="#13ce66"
  inactive-color="#ff4949"
  inactive-text="所有人可见"
  active-text="仅自己可见"
  >
</el-switch>
  <span slot="footer" class="dialog-footer">
    <el-button @click="dialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addNewGraph">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>
<script>
import { mapState } from 'vuex'

import {
  getFashionGraphs,
  getGraphList,
  addGraphApi,
  updateGraphApi
} from '@/api/graph'

export default {
  name: 'graph-list',
  data () {
    return {
      fashionList: [],
      graphList: [],
      dialogVisible: false,
      newGraphName: '',
      isPrivate: true,
      isUpdate: false,
      selectedGraph: null,
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.graph.name,
      gid: state => state.graph.id,
    })
  },
  created () {
    getFashionGraphs().then((response) => {
      this.fashionList = response.data
      if (this.fashionList.length > 0) {
        this.$store.commit('setGraph', this.fashionList[0])
        this.$store.dispatch('getNodesByGraph', {gid: this.fashionList[0].id})
      }
    })
    if (this.user_id) {
      getGraphList(this.user_id).then((response) => {
        this.graphList = response.data
      })
    }
  },
  methods: {
    showAddGraphDialog () {
      this.isUpdate = false
      this.dialogVisible = true
    },
    addNewGraph () {
      if (!this.isUpdate) {
        addGraphApi(this.user_id, this.newGraphName, this.isPrivate).then((response) => {
        this.graphList.push({id: response.data, name: this.newGraphName})
        this.newGraphName = ''
        this.dialogVisible = false
      })
      }
      else {
        updateGraphApi(this.gid, this.newGraphName, this.isPrivate).then((response => {
          this.$store.commit('setGraphName', this.newGraphName)
          this.selectedGraph.name = this.newGraphName
          this.newGraphName = ''
          this.dialogVisible = false
        }))
      }
      
    },
    showEditGraphDialog () {
      this.isUpdate = true
      this.dialogVisible = true
      this.newGraphName = this.name
    },
    deleteGraph () {

    },
    clickGraph (graph) {
      this.selectedGraph = graph
      this.$store.commit('setGraph', {graph})
      this.$store.dispatch('getNodesByGraph', {gid: graph.id})
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
.el-switch {
  padding-top: 20px;
}
</style>
