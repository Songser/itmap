<template>
  <div>
    <div class="buttons">
      <el-button type="primary" icon="el-icon-news" circle @click="showAddGraphDialog"></el-button>
      <el-button type="primary" icon="el-icon-edit" circle @click="showEditGraphDialog"></el-button>
      <el-button type="primary" icon="el-icon-delete" circle @click="showDeleteGraphDialog"></el-button>
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
        active-text="仅自己可见">
      </el-switch>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addNewGraph">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="删除图谱"
      :visible.sync="dialogDelVisible"
      width="50%" :append-to-body=true>
      <span>确定删除图谱: {{name}}</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogDelVisible = false">取 消</el-button>
        <el-button type="primary" @click="delGraph">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import { Message } from 'element-ui'
import {
  getFashionGraphs,
  getGraphList,
  addGraphApi,
  updateGraphApi,
  deleteGraphApi
} from '@/api/graph'

export default {
  name: 'graph-list',
  data () {
    return {
      fashionList: [],
      graphList: [],
      dialogVisible: false,
      dialogDelVisible: false,
      newGraphName: '',
      isPrivate: true,
      isUpdate: false,
      selectedGraph: null
    }
  },
  computed: {
    ...mapState({
      userId: state => state.user.id,
      name: state => state.graph.name,
      gid: state => state.graph.id
    })
  },
  created () {
    getFashionGraphs().then(response => {
      this.fashionList = response.data
      if (this.fashionList.length > 0) {
        this.selectedGraph = this.fashionList[0]
        this.$store.commit('setGraph', this.fashionList[0])
        this.$store.dispatch('getNodesByGraph', {
          gid: this.fashionList[0].id
        })
      }
    })
    if (this.userId) {
      getGraphList(this.userId).then(response => {
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
        addGraphApi(this.userId, this.newGraphName, this.isPrivate).then(
          response => {
            this.graphList.push({ id: response.data, name: this.newGraphName })
            this.newGraphName = ''
            this.dialogVisible = false
          }
        )
      } else {
        updateGraphApi(this.gid, this.newGraphName, this.isPrivate).then(
          response => {
            this.$store.commit('setGraphName', this.newGraphName)
            this.selectedGraph.name = this.newGraphName
            this.newGraphName = ''
            this.dialogVisible = false
          }
        )
      }
    },
    showEditGraphDialog () {
      this.isUpdate = true
      this.dialogVisible = true
      this.newGraphName = this.name
    },
    showDeleteGraphDialog () {
      this.dialogDelVisible = true
    },
    clickGraph (graph) {
      this.selectedGraph = graph
      this.$store.commit('setGraph', { graph })
      this.$store.dispatch('getNodesByGraph', { gid: graph.id })
    },
    delGraph () {
      if (this.selectedGraph.owner_id !== this.$store.state.user.id) {
        Message({
          message: '无法删除图谱' + this.name,
          type: 'info',
          duration: 3 * 1000
        })
      } else {
        deleteGraphApi(this.gid).then(response => {
          console.log(this.selectedGraph)
          let value = []
          for (let graph of this.graphList) {
            if (graph.id !== this.gid) {
              value.push(graph)
            }
          }
          this.graphList = value
          this.clickGraph(this.graphList[0])
        })
      }
      this.dialogDelVisible = false
    }
  }
}
</script>

<style scoped>
.buttons {
  margin: 10px 0;
  text-align: center;
}
.el-button {
  margin: 0;
}
.el-dialog {
  text-align: left;
}
.el-switch {
  padding-top: 20px;
}
</style>
