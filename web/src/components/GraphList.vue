<template>
  <div>
    <div class="buttons">
      <el-button type="primary" icon="el-icon-news" circle @click="addGraph"></el-button>
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
     <el-menu-item index="2">
        <i class="el-icon-menu"></i>
        <span slot="title">主图谱</span>
      </el-menu-item>
    </el-menu>
    
  </div>
</template>
<script>

function getGraphs(){

}
export default {
  name: 'graph-list',
  created () {

  },
  methods: {
      addGraph (){
        
      },
      editGraph () {

      },
      deleteGraph () {

      }
  }
}
</script>

<style scoped>
.buttons {
  margin: 10px;
  text-align: left;
}
</style>